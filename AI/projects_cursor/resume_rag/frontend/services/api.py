import time

import requests
from requests.exceptions import ConnectionError, HTTPError, Timeout

from config import API_BASE_URL

_DEFAULT_RETRIES = 8
_DEFAULT_RETRY_DELAY = 2


def _extract_error_detail(response: requests.Response) -> str:
    try:
        body = response.json()
        detail = body.get("detail")
        if isinstance(detail, list):
            return "; ".join(str(item) for item in detail)
        if detail:
            return str(detail)
    except Exception:
        pass
    return response.text or f"HTTP {response.status_code}"


def _request_with_retry(method, url, *, retries=_DEFAULT_RETRIES, retry_delay=_DEFAULT_RETRY_DELAY, **kwargs):
    last_exc = None
    for attempt in range(retries):
        try:
            response = requests.request(method, url, **kwargs)
            if not response.ok:
                raise HTTPError(
                    _extract_error_detail(response),
                    response=response,
                )
            return response.json()
        except (ConnectionError, Timeout) as exc:
            last_exc = exc
            if attempt < retries - 1:
                time.sleep(retry_delay)
        except HTTPError:
            raise
    raise last_exc


class ApiClient:
    @staticmethod
    def get(endpoint, timeout=30):
        return _request_with_retry(
            "GET",
            f"{API_BASE_URL}{endpoint}",
            timeout=timeout,
        )

    @staticmethod
    def post(endpoint, json=None, files=None, data=None, timeout=120):
        return _request_with_retry(
            "POST",
            f"{API_BASE_URL}{endpoint}",
            json=json,
            files=files,
            data=data,
            timeout=timeout,
        )

import requests

from config import API_BASE_URL


class ApiClient:
    @staticmethod
    def get(endpoint, timeout=30):
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=timeout)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def post(endpoint, json=None, files=None, data=None, timeout=120):
        response = requests.post(
            f"{API_BASE_URL}{endpoint}",
            json=json,
            files=files,
            data=data,
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()

import requests

from config import API_BASE_URL


class ApiClient:

    @staticmethod
    def get(endpoint):

        response = requests.get(
            f"{API_BASE_URL}{endpoint}"
        )

        response.raise_for_status()

        return response.json()

    @staticmethod
    def post(
        endpoint,
        json=None,
        files=None,
        data=None
    ):

        response = requests.post(
            f"{API_BASE_URL}{endpoint}",
            json=json,
            files=files,
            data=data
        )

        response.raise_for_status()

        return response.json()
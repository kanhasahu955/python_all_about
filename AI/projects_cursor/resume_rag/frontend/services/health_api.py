from services.api import ApiClient


class HealthApi:
    @staticmethod
    def connections():
        return ApiClient.get("/connections")

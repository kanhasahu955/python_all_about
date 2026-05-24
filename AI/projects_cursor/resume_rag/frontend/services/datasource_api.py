from services.api import ApiClient


class DatasourceApi:
    @staticmethod
    def list_datasources():
        return ApiClient.get("/datasources/")

    @staticmethod
    def test_connection(payload):
        return ApiClient.post("/datasources/test", json=payload)

    @staticmethod
    def test_app_database():
        return ApiClient.get("/datasources/app-db/test")

    @staticmethod
    def create_datasource(payload):
        return ApiClient.post("/datasources/", json=payload)

    @staticmethod
    def test_saved(datasource_id):
        return ApiClient.post(f"/datasources/{datasource_id}/test")

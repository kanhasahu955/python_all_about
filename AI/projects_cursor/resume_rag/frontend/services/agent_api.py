from services.api import ApiClient


class AgentApi:
    @staticmethod
    def list_runs(document_id=None, limit=100):
        params = f"?limit={limit}"
        if document_id:
            params += f"&document_id={document_id}"
        return ApiClient.get(f"/agents/runs{params}")

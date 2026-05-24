from services.api import ApiClient


class RagApi:
    @staticmethod
    def search(query, top_k=5):
        return ApiClient.post("/rag/search", json={"query": query, "top_k": top_k})

    @staticmethod
    def reindex(document_id=None):
        payload = {}
        if document_id:
            payload["document_id"] = document_id
        return ApiClient.post("/rag/reindex", json=payload)

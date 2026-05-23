from services.api import ApiClient


class RagApi:
    @staticmethod
    def search(query, top_k=5):
        return ApiClient.post("/rag/search", json={"query": query, "top_k": top_k})

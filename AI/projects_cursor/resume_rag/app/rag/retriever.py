from app.core.config import settings
from app.rag.embeddings import get_embedding_model
from app.rag.pinecone_store import PineconeStore


class ResumeRetriever:
    def __init__(self):
        self.store = PineconeStore()
        self.embeddings = get_embedding_model()

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        if not self.store.enabled or not settings.OPENAI_API_KEY:
            return []

        vector = self.embeddings.embed_query(query)
        result = self.store.query(vector, top_k=top_k)

        return [
            {
                "id": match.id,
                "score": match.score,
                "metadata": match.metadata or {},
            }
            for match in result.matches
        ]

from app.core.config import settings
from app.rag.embeddings import embeddings_configured, get_embedding_model
from app.rag.pinecone_store import PineconeStore


class ResumeRetriever:
    def __init__(self):
        self.store = PineconeStore()
        self.embeddings = get_embedding_model() if embeddings_configured() else None

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        if not self.store.enabled:
            raise RuntimeError("PINECONE_API_KEY is not configured")
        if not embeddings_configured():
            raise RuntimeError("OPENAI_API_KEY is required for embeddings")

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

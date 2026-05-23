from app.core.config import settings


class PineconeStore:
    def __init__(self):
        self._index = None
        self._enabled = bool(settings.PINECONE_API_KEY)

    @property
    def enabled(self) -> bool:
        return self._enabled

    def _get_index(self):
        if not self._enabled:
            raise RuntimeError("PINECONE_API_KEY is not configured")

        if self._index is None:
            from pinecone import Pinecone

            pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            self._index = pc.Index(settings.PINECONE_INDEX_NAME)

        return self._index

    def upsert_documents(self, vectors: list[dict]):
        if not vectors:
            return

        index = self._get_index()
        index.upsert(vectors=vectors, namespace=settings.PINECONE_NAMESPACE)

    def query(self, vector: list[float], top_k: int = 5):
        index = self._get_index()
        return index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True,
            namespace=settings.PINECONE_NAMESPACE,
        )

from app.core.config import settings


class PineconeStore:
    EMBEDDING_DIMENSION = 1536  # text-embedding-3-small

    def __init__(self):
        self._index = None
        self._client = None
        self._enabled = bool(settings.PINECONE_API_KEY)

    @property
    def enabled(self) -> bool:
        return self._enabled

    def _get_client(self):
        if self._client is None:
            from pinecone import Pinecone

            self._client = Pinecone(api_key=settings.PINECONE_API_KEY)
        return self._client

    def _ensure_index(self):
        from pinecone import ServerlessSpec

        pc = self._get_client()
        name = settings.PINECONE_INDEX_NAME

        if not pc.has_index(name):
            region = settings.PINECONE_ENV or "us-east-1"
            pc.create_index(
                name=name,
                dimension=self.EMBEDDING_DIMENSION,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region=region),
            )

    def _get_index(self):
        if not self._enabled:
            raise RuntimeError("PINECONE_API_KEY is not configured")

        if self._index is None:
            self._ensure_index()
            self._index = self._get_client().Index(settings.PINECONE_INDEX_NAME)

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

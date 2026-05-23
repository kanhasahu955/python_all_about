import uuid

from app.core.config import settings
from app.rag.chunking import chunk_text
from app.rag.embeddings import get_embedding_model
from app.rag.pinecone_store import PineconeStore


class RAGService:
    def __init__(self):
        self.store = PineconeStore()
        self.embeddings = get_embedding_model() if settings.OPENAI_API_KEY else None

    def index_text(self, document_id: str, text: str):
        if not self.store.enabled or not self.embeddings:
            return {
                "document_id": document_id,
                "chunks": 0,
                "indexed": False,
                "message": "Pinecone/OpenAI not configured; skipping index",
            }

        chunks = chunk_text(text)
        vectors = []

        for i, chunk in enumerate(chunks):
            vector = self.embeddings.embed_query(chunk)
            vectors.append(
                {
                    "id": f"{document_id}-{i}-{uuid.uuid4().hex[:8]}",
                    "values": vector,
                    "metadata": {
                        "document_id": document_id,
                        "chunk_index": i,
                        "text": chunk,
                    },
                }
            )

        self.store.upsert_documents(vectors)

        return {
            "document_id": document_id,
            "chunks": len(chunks),
            "indexed": True,
        }

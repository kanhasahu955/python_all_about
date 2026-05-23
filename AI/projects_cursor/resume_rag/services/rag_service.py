import uuid
from app.rag.chunking import chunk_text
from app.rag.embeddings import get_embedding_model
from app.rag.pinecone_store import PineconeStore


class RAGService:
    def __init__(self):
        self.embeddings = get_embedding_model()
        self.store = PineconeStore()

    def index_text(self, document_id: str, text: str):
        chunks = chunk_text(text)

        vectors = []

        for i, chunk in enumerate(chunks):
            vector = self.embeddings.embed_query(chunk)

            vectors.append(
                {
                    "id": f"{document_id}-{i}-{uuid.uuid4()}",
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
        }
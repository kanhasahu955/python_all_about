from rag.pinecone_store import index
from rag.embeddings import embeddings

class ResumeRetriever:

    def search(self, query):

        vector = embeddings.embed_query(query)

        result = index.query(
            vector=vector,
            top_k=10,
            include_metadata=True
        )

        return result.matches
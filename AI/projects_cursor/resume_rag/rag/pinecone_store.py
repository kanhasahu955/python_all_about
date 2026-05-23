from pinecone import Pinecone

pc = Pinecone(
    api_key="YOUR_KEY"
)

index = pc.Index(
    "resume-index"
)
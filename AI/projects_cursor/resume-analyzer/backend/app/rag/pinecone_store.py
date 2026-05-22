from typing import Any

from pinecone import Pinecone

from app.config import settings
from app.rag.embeddings import get_embeddings


def _client() -> Pinecone:
    if not settings.pinecone_api_key:
        raise RuntimeError("PINECONE_API_KEY is not set")
    return Pinecone(api_key=settings.pinecone_api_key)


def get_index():
    pc = _client()
    return pc.Index(settings.pinecone_index_name)


async def upsert_resume_chunks(
    namespace: str,
    chunk_texts: list[str],
    base_metadata: dict[str, Any],
) -> None:
    embeddings = get_embeddings()
    vectors: list[dict[str, Any]] = []
    for i, text in enumerate(chunk_texts):
        vec = await embeddings.aembed_query(text)
        vid = f"{base_metadata.get('resume_external_id', 'r')}-{i}"
        vectors.append(
            {
                "id": vid,
                "values": vec,
                "metadata": {**base_metadata, "chunk_index": i, "text": text[:4000]},
            }
        )
    if not vectors:
        return
    index = get_index()
    # Pinecone upsert in batches if needed
    batch = 100
    for start in range(0, len(vectors), batch):
        index.upsert(vectors=vectors[start : start + batch], namespace=namespace)


async def query_similar(
    namespace: str,
    query: str,
    top_k: int = 8,
) -> list[dict[str, Any]]:
    embeddings = get_embeddings()
    qv = await embeddings.aembed_query(query)
    index = get_index()
    res = index.query(
        vector=qv,
        top_k=top_k,
        namespace=namespace,
        include_metadata=True,
    )
    matches = getattr(res, "matches", None) or []
    out: list[dict[str, Any]] = []
    for m in matches:
        meta = getattr(m, "metadata", None) or {}
        if isinstance(meta, dict):
            text = meta.get("text", "")
            chunk_index = meta.get("chunk_index")
        else:
            text = ""
            chunk_index = None
        score = getattr(m, "score", None)
        out.append({"score": score, "text": text, "chunk_index": chunk_index})
    return out

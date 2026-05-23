from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.retriever import ResumeRetriever
from app.services.rag_service import RAGService

router = APIRouter()


class IndexTextRequest(BaseModel):
    document_id: str
    text: str


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


@router.post("/index")
def index_text(payload: IndexTextRequest):
    return RAGService().index_text(payload.document_id, payload.text)


@router.post("/search")
def search(payload: SearchRequest):
    matches = ResumeRetriever().search(payload.query, payload.top_k)
    return {"query": payload.query, "results": matches}

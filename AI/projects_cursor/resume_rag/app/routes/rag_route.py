from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from app.core.database import engine
from app.models.resume_model import ResumeDocument
from app.rag.retriever import ResumeRetriever
from app.services.rag_service import RAGService

router = APIRouter()


class IndexTextRequest(BaseModel):
    document_id: str
    text: str


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


class ReindexRequest(BaseModel):
    document_id: str | None = None


@router.post("/index")
def index_text(payload: IndexTextRequest):
    return RAGService().index_text(payload.document_id, payload.text)


@router.post("/search")
def search(payload: SearchRequest):
    try:
        matches = ResumeRetriever().search(payload.query, payload.top_k)
        return {"query": payload.query, "results": matches}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.post("/reindex")
def reindex(payload: ReindexRequest):
    """Re-index resume text from DB into Pinecone (use after fixing Pinecone config)."""
    service = RAGService()
    indexed = []

    with Session(engine) as session:
        query = select(ResumeDocument)
        if payload.document_id:
            query = query.where(ResumeDocument.document_id == payload.document_id)
        docs = session.exec(query).all()

        for doc in docs:
            if not doc.content_text:
                continue
            result = service.index_text(doc.document_id, doc.content_text)
            indexed.append(result)

    return {"indexed_documents": len(indexed), "details": indexed}

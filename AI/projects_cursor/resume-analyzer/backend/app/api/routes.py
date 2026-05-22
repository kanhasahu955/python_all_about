import json
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.graph import graph_app
from app.api.schemas import AnalyzeRequest, AnalyzeResponse, ResumeCreated
from app.db.models import Analysis, Resume
from app.db.session import get_db
from app.rag.chunking import chunk_text
from app.rag.pinecone_store import upsert_resume_chunks
from app.utils.pdf import extract_text_from_pdf

router = APIRouter(prefix="/api")


@router.post("/resumes", response_model=ResumeCreated)
async def upload_resume(
    session: Annotated[AsyncSession, Depends(get_db)],
    file: UploadFile | None = File(None),
    text: str | None = Form(None),
    user_label: str | None = Form(None),
):
    raw: str | None = None
    if file and file.filename:
        data = await file.read()
        lower = (file.filename or "").lower()
        if lower.endswith(".pdf"):
            raw = extract_text_from_pdf(data)
        else:
            raw = data.decode("utf-8", errors="replace")
    elif text:
        raw = text
    if not raw or not raw.strip():
        raise HTTPException(400, "Provide a PDF file or text body")

    external_id = str(uuid.uuid4())
    namespace = f"resume-{external_id}"
    chunks = chunk_text(raw)
    if not chunks:
        raise HTTPException(400, "Could not chunk resume text")

    await upsert_resume_chunks(
        namespace,
        chunks,
        base_metadata={"resume_external_id": external_id},
    )

    row = Resume(
        external_id=external_id,
        user_label=user_label,
        raw_text=raw,
        pinecone_namespace=namespace,
    )
    session.add(row)
    await session.commit()

    return ResumeCreated(
        resume_external_id=external_id,
        pinecone_namespace=namespace,
        chunks_indexed=len(chunks),
    )


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    body: AnalyzeRequest,
    session: Annotated[AsyncSession, Depends(get_db)],
):
    q = await session.execute(
        select(Resume).where(Resume.external_id == body.resume_external_id)
    )
    resume = q.scalar_one_or_none()
    if not resume:
        raise HTTPException(404, "Resume not found")

    final = await graph_app.ainvoke(
        {
            "namespace": resume.pinecone_namespace,
            "job_description": body.job_description,
            "context_chunks": [],
            "analysis": None,
        }
    )
    analysis = final.get("analysis")
    if not analysis:
        raise HTTPException(500, "Agent did not return analysis")

    payload = analysis.model_dump()
    row = Analysis(
        resume_id=resume.id,
        job_description=body.job_description,
        result_json=json.dumps(payload),
    )
    session.add(row)
    await session.commit()
    await session.refresh(row)

    return AnalyzeResponse(
        fit_score=analysis.fit_score,
        strengths=analysis.strengths,
        gaps=analysis.gaps,
        suggestions=analysis.suggestions,
        summary=analysis.summary,
        analysis_id=row.id,
    )

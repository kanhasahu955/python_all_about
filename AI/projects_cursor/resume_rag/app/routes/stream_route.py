from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlmodel import Session

from app.core.database import get_session
from app.repository.resume_repository import ResumeRepository
from app.schemas.resume_schema import InterviewRequest, ResumeBuildRequest
from app.services.interview_service import start_interview_session
from app.services.resume_build_service import build_resume_prompt
from app.streaming.analysis_stream import analysis_event_stream
from app.streaming.dashboard_stream import dashboard_event_stream
from app.streaming.interview_stream import interview_event_stream
from app.streaming.sse import create_llm_stream

router = APIRouter()


class StreamRequest(BaseModel):
    prompt: str


class InterviewStartResponse(BaseModel):
    session_id: str


@router.get("/dashboard")
async def stream_dashboard():
    return StreamingResponse(
        dashboard_event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/analysis/{document_id}")
async def stream_analysis(document_id: str):
    return StreamingResponse(
        analysis_event_stream(document_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/interview/start", response_model=InterviewStartResponse)
def start_interview_stream(payload: InterviewRequest):
    session_id = start_interview_session(
        skills=payload.skills,
        document_id=payload.document_id,
    )
    return InterviewStartResponse(session_id=session_id)


@router.get("/interview/{session_id}")
async def stream_interview(session_id: str):
    return StreamingResponse(
        interview_event_stream(session_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/build")
async def stream_build(payload: ResumeBuildRequest, session: Session = Depends(get_session)):
    jd_match = ""
    if payload.document_id:
        analysis = ResumeRepository(session).get_analysis(payload.document_id)
        if analysis and analysis.jd_match_json:
            jd_match = analysis.jd_match_json

    prompt = build_resume_prompt(
        resume_text=payload.resume_text,
        job_description=payload.job_description,
        jd_match_json=jd_match,
    )
    return create_llm_stream(prompt)


@router.post("/llm")
async def stream_llm(request: StreamRequest):
    return create_llm_stream(request.prompt)

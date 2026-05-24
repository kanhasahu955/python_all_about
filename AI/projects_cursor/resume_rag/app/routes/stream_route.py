from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.schemas.resume_schema import InterviewRequest
from app.services.interview_service import start_interview_session
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


@router.post("/llm")
async def stream_llm(request: StreamRequest):
    return create_llm_stream(request.prompt)

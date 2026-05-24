from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.core.database import get_session
from app.repository.agent_repository import AgentRepository
from app.services.agent_events import agent_events

router = APIRouter()


@router.get("/runs")
def list_agent_runs(
    document_id: str | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    session: Session = Depends(get_session),
):
    runs = AgentRepository(session).list_runs(document_id=document_id, limit=limit)
    return [
        {
            "run_id": run.run_id,
            "document_id": run.document_id,
            "agent": run.agent_name,
            "status": run.status,
            "input_json": run.input_json,
            "output_json": run.output_json,
            "created_at": run.created_at.isoformat() if run.created_at else None,
        }
        for run in runs
    ]


@router.get("/runs/{document_id}/events")
def get_agent_events(document_id: str):
    return {"document_id": document_id, "events": agent_events.get_buffer(document_id)}

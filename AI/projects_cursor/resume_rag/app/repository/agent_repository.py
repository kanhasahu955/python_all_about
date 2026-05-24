import json

from sqlmodel import Session, select

from app.models.agent_model import AgentRun


class AgentRepository:
    def __init__(self, session: Session):
        self.session = session

    def record_run(
        self,
        document_id: str,
        agent_name: str,
        status: str,
        *,
        input_json: str | None = None,
        output_json: str | None = None,
    ) -> AgentRun:
        run = AgentRun(
            document_id=document_id,
            agent_name=agent_name,
            status=status,
            input_json=input_json,
            output_json=output_json,
        )
        self.session.add(run)
        self.session.commit()
        self.session.refresh(run)
        return run

    def list_runs(
        self,
        *,
        document_id: str | None = None,
        limit: int = 100,
    ) -> list[AgentRun]:
        query = select(AgentRun).order_by(AgentRun.created_at.desc()).limit(limit)
        if document_id:
            query = query.where(AgentRun.document_id == document_id)
        return list(self.session.exec(query))

    @staticmethod
    def serialize_output(state: dict) -> str:
        safe: dict = {}
        for key, value in state.items():
            if isinstance(value, str) and len(value) > 2000:
                safe[key] = value[:2000] + "..."
            else:
                safe[key] = value
        return json.dumps(safe, default=str)

from sqlmodel import Session

from app.core.database import engine
from app.core.redis_client import get_queue
from app.hooks.langfuse_hooks import trace_resume_run
from app.langgraph.resume_graph import resume_graph
from app.models.resume_model import ResumeAnalysis, ResumeStatus
from app.repository.agent_repository import AgentRepository
from app.repository.resume_repository import ResumeRepository
from app.services.agent_events import agent_events
from app.services.rag_service import RAGService


def _mark_resume_failed(document_id: str, error: str) -> None:
    with Session(engine) as session:
        ResumeRepository(session).update_status(document_id, ResumeStatus.failed)
    agent_events.publish_pipeline_failed(document_id, error)


def on_analysis_job_failure(job, connection, type, value, traceback):  # noqa: ARG001
    document_id = job.args[0] if job.args else None
    if document_id:
        _mark_resume_failed(document_id, str(value))


def enqueue_resume_analysis(
    document_id: str,
    file_path: str,
    job_description: str | None = None,
) -> str:
    job = get_queue().enqueue(
        run_resume_analysis_job,
        document_id,
        file_path,
        job_description,
        job_timeout=600,
        on_failure=on_analysis_job_failure,
    )
    return job.id


def _run_graph_with_tracking(document_id: str, initial_state: dict) -> dict:
    state = dict(initial_state)

    with Session(engine) as session:
        repo = ResumeRepository(session)
        doc = repo.get_by_document_id(document_id)
        if doc:
            doc.status = ResumeStatus.processing
            session.add(doc)
            session.commit()
            agent_events.publish_pipeline_started(document_id, file_name=doc.file_name)

    with Session(engine) as session:
        agent_repo = AgentRepository(session)
        try:
            for step in resume_graph.stream(state):
                for node_name, node_output in step.items():
                    state.update(node_output)
                    agent_repo.record_run(
                        document_id=document_id,
                        agent_name=node_name,
                        status="success",
                        output_json=AgentRepository.serialize_output(node_output),
                    )
                    agent_events.publish_agent_completed(document_id, node_name, state)
        except Exception as exc:
            agent_repo.record_run(
                document_id=document_id,
                agent_name="pipeline",
                status="failed",
                output_json=str(exc),
            )
            agent_events.publish_pipeline_failed(document_id, str(exc))
            raise

    return state


def run_resume_analysis_job(
    document_id: str,
    file_path: str,
    job_description: str | None = None,
):
    try:
        with trace_resume_run(document_id=document_id):
            state = _run_graph_with_tracking(
                document_id,
                {
                    "document_id": document_id,
                    "file_path": file_path,
                    "job_description": job_description or "",
                },
            )

            with Session(engine) as session:
                repo = ResumeRepository(session)
                doc = repo.get_by_document_id(document_id)

                if doc:
                    doc.content_text = state.get("resume_text")
                    doc.status = ResumeStatus.analyzed
                    session.add(doc)

                    analysis = ResumeAnalysis(
                        document_id=document_id,
                        skills_json=state.get("skills_json"),
                        jd_match_json=state.get("jd_match_json"),
                        optimized_resume=state.get("optimized_resume"),
                    )

                    session.add(analysis)
                    session.commit()

            if state.get("resume_text"):
                try:
                    RAGService().index_text(document_id, state["resume_text"])
                    agent_events.publish_rag_indexed(document_id)
                except Exception:
                    pass

            agent_events.publish_pipeline_completed(document_id)
            return state
    except Exception as exc:
        _mark_resume_failed(document_id, str(exc))
        raise

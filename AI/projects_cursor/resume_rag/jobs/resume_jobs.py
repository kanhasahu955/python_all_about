from redis import Redis
from rq import Queue
from sqlmodel import Session

from app.core.config import settings
from app.core.database import engine
from app.langgraph.resume_graph import resume_graph
from app.repository.resume_repository import ResumeRepository
from app.models.resume_model import ResumeStatus, ResumeAnalysis
from app.services.rag_service import RAGService
from app.hooks.langfuse_hooks import trace_resume_run

redis_conn = Redis.from_url(settings.REDIS_URL)
queue = Queue("default", connection=redis_conn)


def enqueue_resume_analysis(
    document_id: str,
    file_path: str,
    job_description: str | None = None,
) -> str:
    job = queue.enqueue(
        run_resume_analysis_job,
        document_id,
        file_path,
        job_description,
        job_timeout=600,
    )
    return job.id


def run_resume_analysis_job(
    document_id: str,
    file_path: str,
    job_description: str | None = None,
):
    with trace_resume_run(document_id=document_id):
        state = resume_graph.invoke(
            {
                "document_id": document_id,
                "file_path": file_path,
                "job_description": job_description or "",
            }
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
                    summary=state.get("jd_match_json"),
                    optimized_resume_markdown=state.get("optimized_resume"),
                )

                session.add(analysis)
                session.commit()

        if state.get("resume_text"):
            RAGService().index_text(document_id, state["resume_text"])

        return state
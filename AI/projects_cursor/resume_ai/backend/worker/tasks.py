"""Background job hooks (replace with Celery/RQ/Arq workers in production)."""

from core.logger import get_logger

log = get_logger(__name__)


def enqueue_resume_reindex(resume_id: int) -> None:
    """Placeholder: e.g. re-embed resume into Pinecone when search is enabled."""
    log.debug("worker stub enqueue_resume_reindex resume_id=%s", resume_id)


def enqueue_resume_export(resume_id: int, format: str = "pdf") -> None:
    """Placeholder: async PDF export pipeline."""
    log.debug(
        "worker stub enqueue_resume_export resume_id=%s format=%s",
        resume_id,
        format,
    )

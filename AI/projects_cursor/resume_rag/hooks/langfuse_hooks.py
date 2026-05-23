from contextlib import contextmanager
from langfuse import Langfuse
from app.core.config import settings


@contextmanager
def trace_resume_run(document_id: str):
    if not settings.LANGFUSE_PUBLIC_KEY or not settings.LANGFUSE_SECRET_KEY:
        yield None
        return

    langfuse = Langfuse(
        public_key=settings.LANGFUSE_PUBLIC_KEY,
        secret_key=settings.LANGFUSE_SECRET_KEY,
        host=settings.LANGFUSE_HOST,
    )

    trace = langfuse.trace(
        name="resume-analysis",
        metadata={"document_id": document_id},
    )

    try:
        yield trace
    finally:
        langfuse.flush()
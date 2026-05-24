import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi import UploadFile
from rq.job import Job
from sqlmodel import Session

from app.core.config import settings
from app.core.redis_client import get_redis
from app.jobs.resume_jobs import enqueue_resume_analysis, run_resume_analysis_job
from app.models.resume_model import ResumeDocument, ResumeStatus
from app.repository.resume_repository import ResumeRepository
from app.utils.paths import resolve_resume_path

_STALE_QUEUED = timedelta(minutes=3)


class ResumeService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = ResumeRepository(session)

    async def upload_resume(self, file: UploadFile, job_description: str | None = None):
        document_id = str(uuid.uuid4())

        storage_dir = Path("storage/resumes")
        storage_dir.mkdir(parents=True, exist_ok=True)

        file_path = storage_dir / f"{document_id}_{file.filename}"
        file_path.write_bytes(await file.read())
        absolute_path = str(file_path.resolve())

        doc = ResumeDocument(
            document_id=document_id,
            file_name=file.filename or "resume",
            file_path=absolute_path,
            status=ResumeStatus.queued,
        )

        self.repo.create_document(doc)

        job_id = None
        if settings.USE_REDIS_QUEUE:
            try:
                job_id = enqueue_resume_analysis(
                    document_id=document_id,
                    file_path=absolute_path,
                    job_description=job_description,
                )
                self.repo.update_job_id(document_id, job_id)
            except Exception as exc:
                self.repo.update_status(document_id, ResumeStatus.failed)
                return {
                    "document_id": document_id,
                    "job_id": None,
                    "status": "failed",
                    "error": f"Redis queue unavailable: {exc}",
                }

        if job_id is None:
            try:
                run_resume_analysis_job(
                    document_id=document_id,
                    file_path=absolute_path,
                    job_description=job_description,
                )
                status = "analyzed"
            except Exception as exc:
                self.repo.update_status(document_id, ResumeStatus.failed)
                return {
                    "document_id": document_id,
                    "job_id": None,
                    "status": "failed",
                    "error": str(exc),
                }
        else:
            status = "queued"

        return {
            "document_id": document_id,
            "job_id": job_id,
            "status": status,
        }

    def sync_document_statuses(self) -> None:
        """Align DB status with RQ job state; mark stale queued docs as failed."""
        if not settings.USE_REDIS_QUEUE:
            return

        now = datetime.now(timezone.utc)
        redis = get_redis()

        for doc in self.repo.list_documents():
            if doc.status in (ResumeStatus.analyzed, ResumeStatus.failed):
                continue

            if doc.job_id:
                try:
                    job = Job.fetch(doc.job_id, connection=redis)
                    rq_status = job.get_status()
                    if rq_status == "failed":
                        self.repo.update_status(doc.document_id, ResumeStatus.failed)
                    continue
                except Exception:
                    pass

            created = doc.created_at
            if created.tzinfo is None:
                created = created.replace(tzinfo=timezone.utc)

            if doc.status == ResumeStatus.queued and now - created > _STALE_QUEUED:
                self.repo.update_status(doc.document_id, ResumeStatus.failed)

    def retry_analysis(self, document_id: str) -> dict | None:
        doc = self.repo.get_by_document_id(document_id)
        if not doc:
            return None

        resolved = resolve_resume_path(doc.file_path)
        if not resolved:
            self.repo.update_status(document_id, ResumeStatus.failed)
            return {
                "document_id": document_id,
                "status": "failed",
                "error": "PDF file missing on disk — re-upload the resume",
            }

        file_path = str(resolved)
        self.repo.update_status(document_id, ResumeStatus.queued)

        if settings.USE_REDIS_QUEUE:
            job_id = enqueue_resume_analysis(
                document_id=document_id,
                file_path=file_path,
                job_description=None,
            )
            self.repo.update_job_id(document_id, job_id)
            return {"document_id": document_id, "job_id": job_id, "status": "queued"}

        try:
            run_resume_analysis_job(document_id=document_id, file_path=file_path)
            return {"document_id": document_id, "job_id": None, "status": "analyzed"}
        except Exception as exc:
            self.repo.update_status(document_id, ResumeStatus.failed)
            return {"document_id": document_id, "status": "failed", "error": str(exc)}

    def list_resumes(self):
        self.sync_document_statuses()
        return self.repo.list_documents()

    def get_resume(self, document_id: str):
        self.sync_document_statuses()
        doc = self.repo.get_by_document_id(document_id)
        if not doc:
            return None

        analysis = self.repo.get_analysis(document_id)
        return {"document": doc, "analysis": analysis}

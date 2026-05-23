import uuid
from pathlib import Path

from fastapi import UploadFile
from sqlmodel import Session

from app.core.config import settings
from app.jobs.resume_jobs import enqueue_resume_analysis, run_resume_analysis_job
from app.models.resume_model import ResumeDocument, ResumeStatus
from app.repository.resume_repository import ResumeRepository


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

        doc = ResumeDocument(
            document_id=document_id,
            file_name=file.filename or "resume",
            file_path=str(file_path),
            status=ResumeStatus.queued,
        )

        self.repo.create_document(doc)

        job_id = None
        if settings.USE_REDIS_QUEUE:
            try:
                job_id = enqueue_resume_analysis(
                    document_id=document_id,
                    file_path=str(file_path),
                    job_description=job_description,
                )
            except Exception:
                job_id = None

        if job_id is None:
            run_resume_analysis_job(
                document_id=document_id,
                file_path=str(file_path),
                job_description=job_description,
            )
            status = "completed"
        else:
            status = "queued"

        return {
            "document_id": document_id,
            "job_id": job_id,
            "status": status,
        }

    def list_resumes(self):
        return self.repo.list_documents()

    def get_resume(self, document_id: str):
        doc = self.repo.get_by_document_id(document_id)
        if not doc:
            return None

        analysis = self.repo.get_analysis(document_id)
        return {"document": doc, "analysis": analysis}

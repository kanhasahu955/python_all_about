import uuid
from pathlib import Path
from fastapi import UploadFile
from sqlmodel import Session

from app.models.resume_model import ResumeDocument
from app.repository.resume_repository import ResumeRepository
from app.jobs.resume_jobs import enqueue_resume_analysis


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
        )

        self.repo.create_document(doc)

        job_id = enqueue_resume_analysis(
            document_id=document_id,
            file_path=str(file_path),
            job_description=job_description,
        )

        return {
            "document_id": document_id,
            "job_id": job_id,
            "status": "queued",
        }
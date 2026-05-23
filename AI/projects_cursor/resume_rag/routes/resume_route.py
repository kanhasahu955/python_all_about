from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlmodel import Session

from app.core.database import get_session
from app.services.resume_service import ResumeService

router = APIRouter()


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    job_description: str | None = Form(default=None),
    session: Session = Depends(get_session),
):
    return await ResumeService(session).upload_resume(file, job_description)
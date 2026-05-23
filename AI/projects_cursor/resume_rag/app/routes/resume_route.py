from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
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


@router.get("/")
def list_resumes(session: Session = Depends(get_session)):
    docs = ResumeService(session).list_resumes()
    return [
        {
            "document_id": d.document_id,
            "file_name": d.file_name,
            "status": d.status,
        }
        for d in docs
    ]


@router.get("/{document_id}")
def get_resume(document_id: str, session: Session = Depends(get_session)):
    result = ResumeService(session).get_resume(document_id)
    if not result:
        raise HTTPException(status_code=404, detail="Resume not found")

    doc = result["document"]
    analysis = result["analysis"]

    return {
        "document_id": doc.document_id,
        "file_name": doc.file_name,
        "status": doc.status,
        "content_text": doc.content_text,
        "analysis": {
            "skills_json": analysis.skills_json if analysis else None,
            "jd_match_json": analysis.jd_match_json if analysis else None,
            "optimized_resume": analysis.optimized_resume if analysis else None,
            "interview_questions": analysis.interview_questions if analysis else None,
            "evaluation_json": analysis.evaluation_json if analysis else None,
        },
    }

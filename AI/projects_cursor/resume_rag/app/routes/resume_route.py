from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlmodel import Session

from app.agents.interview_agent import InterviewAgent
from app.agents.resume_builder_agent import ResumeBuilderAgent
from app.core.database import get_session
from app.repository.resume_repository import ResumeRepository
from app.schemas.resume_schema import InterviewRequest, ResumeBuildRequest
from app.services.resume_service import ResumeService
from app.utils.paths import resolve_resume_path

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
            "status": d.status.value if hasattr(d.status, "value") else d.status,
            "file_exists": resolve_resume_path(d.file_path) is not None,
        }
        for d in docs
    ]


@router.post("/{document_id}/retry")
def retry_resume_analysis(document_id: str, session: Session = Depends(get_session)):
    result = ResumeService(session).retry_analysis(document_id)
    if not result:
        raise HTTPException(status_code=404, detail="Resume not found")
    if result.get("status") == "failed":
        raise HTTPException(
            status_code=400,
            detail=result.get("error", "Retry failed"),
        )
    return result


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
        "status": doc.status.value if hasattr(doc.status, "value") else doc.status,
        "content_text": doc.content_text,
        "analysis": {
            "skills_json": analysis.skills_json if analysis else None,
            "jd_match_json": analysis.jd_match_json if analysis else None,
            "optimized_resume": analysis.optimized_resume if analysis else None,
            "interview_questions": analysis.interview_questions if analysis else None,
            "evaluation_json": analysis.evaluation_json if analysis else None,
        },
    }


@router.post("/build")
def build_resume(payload: ResumeBuildRequest):
    state = ResumeBuilderAgent().execute(
        {
            "resume_text": payload.resume_text,
            "job_description": payload.job_description,
        }
    )
    return {"optimized_resume": state.get("optimized_resume", "")}


@router.post("/interview")
def generate_interview(payload: InterviewRequest, session: Session = Depends(get_session)):
    skills = payload.skills
    resume_text = ""

    if payload.document_id:
        repo = ResumeRepository(session)
        doc = repo.get_by_document_id(payload.document_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Resume not found")
        resume_text = doc.content_text or ""
        analysis = repo.get_analysis(payload.document_id)
        if not skills and analysis and analysis.skills_json:
            skills = analysis.skills_json

    if not skills and not resume_text:
        raise HTTPException(status_code=400, detail="Provide skills, document_id, or both")

    state = InterviewAgent().execute({"skills": skills, "resume_text": resume_text})
    return {"interview_questions": state.get("interview_questions", "")}

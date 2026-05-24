from pydantic import BaseModel


class ResumeUploadResponse(BaseModel):
    document_id: str
    job_id: str
    status: str


class ResumeAnalyzeRequest(BaseModel):
    job_description: str


class ResumeBuildRequest(BaseModel):
    resume_text: str
    job_description: str = ""
    document_id: str | None = None


class ResumeExportRequest(BaseModel):
    content: str
    file_name: str = "optimized_resume"


class InterviewRequest(BaseModel):
    skills: str = ""
    document_id: str | None = None
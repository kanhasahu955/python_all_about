from pydantic import BaseModel


class ResumeUploadResponse(BaseModel):
    document_id: str
    job_id: str
    status: str


class ResumeAnalyzeRequest(BaseModel):
    job_description: str


class ResumeBuildRequest(BaseModel):
    resume_text: str
    job_description: str
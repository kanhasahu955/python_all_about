from pydantic import BaseModel


class ResumeAnalyzeRequest(BaseModel):
    job_description: str


class ResumeBuildRequest(BaseModel):
    candidate_profile: str
    target_role: str
    job_description: str | None = None


class ResumeUploadResponse(BaseModel):
    document_id: str
    job_id: str
    status: str
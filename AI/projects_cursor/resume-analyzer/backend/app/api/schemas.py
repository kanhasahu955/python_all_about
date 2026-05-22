from pydantic import BaseModel, Field


class ResumeCreated(BaseModel):
    resume_external_id: str
    pinecone_namespace: str
    chunks_indexed: int


class AnalyzeRequest(BaseModel):
    resume_external_id: str
    job_description: str = Field(min_length=20)


class AnalyzeResponse(BaseModel):
    fit_score: int
    strengths: list[str]
    gaps: list[str]
    suggestions: list[str]
    summary: str
    analysis_id: int

from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field


class ResumeStatus(str, Enum):
    uploaded = "uploaded"
    parsing = "parsing"
    parsed = "parsed"
    analyzed = "analyzed"
    failed = "failed"


class ResumeDocument(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    document_id: str = Field(index=True, unique=True)
    file_name: str
    file_path: str
    content_text: Optional[str] = None
    status: ResumeStatus = ResumeStatus.uploaded


class ResumeAnalysis(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    document_id: str = Field(index=True)
    candidate_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills_json: Optional[str] = None
    experience_years: Optional[float] = None
    jd_score: Optional[float] = None
    missing_skills_json: Optional[str] = None
    summary: Optional[str] = None
    optimized_resume_markdown: Optional[str] = None
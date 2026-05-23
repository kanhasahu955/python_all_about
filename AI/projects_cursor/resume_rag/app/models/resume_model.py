from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field


class ResumeStatus(str, Enum):
    uploaded = "uploaded"
    queued = "queued"
    processing = "processing"
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
    skills_json: Optional[str] = None
    jd_match_json: Optional[str] = None
    optimized_resume: Optional[str] = None
    interview_questions: Optional[str] = None
    evaluation_json: Optional[str] = None
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlalchemy import Column, DateTime, Text
from sqlmodel import Field, SQLModel


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ResumeStatus(str, Enum):
    uploaded = "uploaded"
    queued = "queued"
    processing = "processing"
    analyzed = "analyzed"
    failed = "failed"


class ResumeDocument(SQLModel, table=True):
    document_id: str = Field(primary_key=True)
    file_name: str
    file_path: str
    content_text: Optional[str] = Field(default=None, sa_column=Column(Text))
    job_id: Optional[str] = Field(default=None)
    status: ResumeStatus = ResumeStatus.uploaded
    created_at: datetime = Field(
        default_factory=_utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )


class ResumeAnalysis(SQLModel, table=True):
    document_id: str = Field(primary_key=True, foreign_key="resumedocument.document_id")
    skills_json: Optional[str] = Field(default=None, sa_column=Column(Text))
    jd_match_json: Optional[str] = Field(default=None, sa_column=Column(Text))
    optimized_resume: Optional[str] = Field(default=None, sa_column=Column(Text))
    interview_questions: Optional[str] = Field(default=None, sa_column=Column(Text))
    evaluation_json: Optional[str] = Field(default=None, sa_column=Column(Text))

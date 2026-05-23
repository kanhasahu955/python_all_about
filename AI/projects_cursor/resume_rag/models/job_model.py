from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field


class JobStatus(str, Enum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"


class BackgroundJob(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: str = Field(index=True, unique=True)
    job_type: str
    status: JobStatus = JobStatus.queued
    payload_json: Optional[str] = None
    result_json: Optional[str] = None
    error: Optional[str] = None
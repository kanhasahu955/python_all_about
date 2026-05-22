from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ExperienceItem(BaseModel):
    title: str = ""
    company: str = ""
    location: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    highlights: list[str] = Field(default_factory=list)


class EducationItem(BaseModel):
    school: str = ""
    degree: str | None = None
    field: str | None = None
    end_date: str | None = None


class ResumeContentV1(BaseModel):
    """Structured resume body stored in ``Resume.content`` and produced by the AI agent."""

    headline: str = ""
    summary: str = ""
    skills: list[str] = Field(default_factory=list)
    experience: list[ExperienceItem] = Field(default_factory=list)
    education: list[EducationItem] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)


class ResumeCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: dict[str, Any] | None = None
    status: str = Field(default="draft", max_length=32)
    job_target: str | None = None


class ResumeUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    content: dict[str, Any] | None = None
    status: str | None = Field(default=None, max_length=32)
    job_target: str | None = None


class ResumeRead(BaseModel):
    id: int
    title: str
    content: dict[str, Any]
    status: str
    job_target: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PaginatedResumes(BaseModel):
    items: list[ResumeRead]
    total: int
    limit: int
    offset: int


class AIImproveRequest(BaseModel):
    section: str = Field(
        min_length=1,
        description="Logical section name, e.g. summary, experience_block",
    )
    text: str = Field(min_length=1)
    job_description: str | None = None
    tone: str = Field(default="professional, concise, ATS-friendly")


class AIImproveResponse(BaseModel):
    improved_text: str


class AIAgentBuildRequest(BaseModel):
    """Raw notes, prior resume paste, or bullet dump — the agent extracts and structures."""

    profile_notes: str = Field(min_length=10)
    job_description: str | None = None


class AIAgentBuildResponse(BaseModel):
    content: ResumeContentV1
    steps_completed: list[str]

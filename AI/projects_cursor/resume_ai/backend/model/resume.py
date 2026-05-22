from typing import Any

from sqlalchemy import JSON, Column, Text
from sqlmodel import Field, SQLModel

from model.base import TimestampMixin


class Resume(TimestampMixin, SQLModel, table=True):
    __tablename__ = "resumes"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=255, index=True)
    content: dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column(JSON, nullable=False),
    )
    status: str = Field(default="draft", max_length=32, index=True)
    job_target: str | None = Field(default=None, sa_column=Column(Text, nullable=True))

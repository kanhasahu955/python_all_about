from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from core.config import Settings, get_settings
from core.database import get_db
from services.ai_service import AIService
from services.resume_service import ResumeService


DbSession = Annotated[Session, Depends(get_db)]


def get_resume_service(session: DbSession) -> ResumeService:
    return ResumeService(session)


def get_ai_service(
    settings: Annotated[Settings, Depends(get_settings)],
) -> AIService:
    return AIService(settings)

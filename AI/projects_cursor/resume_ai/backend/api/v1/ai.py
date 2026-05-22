from typing import Annotated

from fastapi import APIRouter, Depends

from api.deps import get_ai_service
from schema.resume import (
    AIAgentBuildRequest,
    AIAgentBuildResponse,
    AIImproveRequest,
    AIImproveResponse,
)
from services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/improve", response_model=AIImproveResponse)
async def improve_text(
    body: AIImproveRequest,
    service: Annotated[AIService, Depends(get_ai_service)],
) -> AIImproveResponse:
    return await service.improve_section(
        section=body.section,
        text=body.text,
        job_description=body.job_description,
        tone=body.tone,
    )


@router.post("/agent/build", response_model=AIAgentBuildResponse)
async def agent_build_resume(
    body: AIAgentBuildRequest,
    service: Annotated[AIService, Depends(get_ai_service)],
) -> AIAgentBuildResponse:
    content, steps = await service.agent_build_resume(
        profile_notes=body.profile_notes,
        job_description=body.job_description,
    )
    return AIAgentBuildResponse(content=content, steps_completed=steps)

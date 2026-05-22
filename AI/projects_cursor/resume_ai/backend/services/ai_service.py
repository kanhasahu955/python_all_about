from ai.improve import improve_section as improve_section_llm
from ai.llm import create_async_client
from ai.resume_agent import run_resume_build_agent
from core.config import Settings
from schema.resume import AIImproveResponse, ResumeContentV1


class AIService:
    """Facades LLM calls implemented under ``ai/``."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = create_async_client(settings)

    async def improve_section(
        self,
        *,
        section: str,
        text: str,
        job_description: str | None,
        tone: str,
    ) -> AIImproveResponse:
        return await improve_section_llm(
            self._client,
            self._settings,
            section=section,
            text=text,
            job_description=job_description,
            tone=tone,
        )

    async def agent_build_resume(
        self,
        *,
        profile_notes: str,
        job_description: str | None,
    ) -> tuple[ResumeContentV1, list[str]]:
        return await run_resume_build_agent(
            self._client,
            self._settings,
            profile_notes=profile_notes,
            job_description=job_description,
        )

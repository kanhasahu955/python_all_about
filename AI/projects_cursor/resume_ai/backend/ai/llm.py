"""OpenAI client construction from app settings."""

from openai import AsyncOpenAI

from core.config import Settings


def create_async_client(settings: Settings) -> AsyncOpenAI:
    return AsyncOpenAI(
        api_key=settings.OPENAI_API_KEY,
        timeout=settings.OPENAI_TIMEOUT_SECONDS,
    )

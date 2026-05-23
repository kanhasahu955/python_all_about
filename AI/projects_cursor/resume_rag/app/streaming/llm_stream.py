from typing import AsyncGenerator

from app.core.config import settings


def _get_llm():
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model="gpt-4o-mini",
        api_key=settings.OPENAI_API_KEY,
        streaming=True,
    )


async def stream_llm_response(prompt: str) -> AsyncGenerator[str, None]:
    if not settings.OPENAI_API_KEY:
        yield "data: OPENAI_API_KEY is not configured\n\n"
        return

    llm = _get_llm()
    async for chunk in llm.astream(prompt):
        if chunk.content:
            yield f"data: {chunk.content}\n\n"

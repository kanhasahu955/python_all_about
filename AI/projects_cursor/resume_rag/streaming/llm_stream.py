from typing import AsyncGenerator

from langchain_openai import ChatOpenAI
from app.core.config import settings


llm = ChatOpenAI(
    model="gpt-4o",
    api_key=settings.OPENAI_API_KEY,
    streaming=True,
)


async def stream_llm_response(
    prompt: str,
) -> AsyncGenerator[str, None]:

    async for chunk in llm.astream(prompt):

        if chunk.content:
            yield f"data: {chunk.content}\n\n"
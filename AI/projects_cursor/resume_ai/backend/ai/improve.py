"""Single-shot section improvement."""

from openai import AsyncOpenAI

from ai import prompts
from core.config import Settings
from schema.resume import AIImproveResponse
from utils.json_text import parse_llm_json_object


async def improve_section(
    client: AsyncOpenAI,
    settings: Settings,
    *,
    section: str,
    text: str,
    job_description: str | None,
    tone: str,
) -> AIImproveResponse:
    user = f"Section: {section}\nTone: {tone}\n\nText to improve:\n{text}"
    if job_description:
        user += f"\n\nJob description:\n{job_description}"

    resp = await client.chat.completions.create(
        model=settings.LLM_MODEL,
        max_tokens=min(2048, settings.AI_AGENT_MAX_COMPLETION_TOKENS),
        messages=[
            {"role": "system", "content": prompts.IMPROVE_SYSTEM},
            {"role": "user", "content": user},
        ],
        response_format={"type": "json_object"},
    )
    raw = resp.choices[0].message.content or "{}"
    data = parse_llm_json_object(raw)
    return AIImproveResponse(improved_text=str(data.get("improved_text", "")).strip())

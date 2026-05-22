"""Multi-step agent: extract facts → synthesize structured resume."""

import json

from openai import AsyncOpenAI

from ai import prompts
from core.config import Settings
from core.logger import get_logger
from schema.resume import ResumeContentV1
from utils.json_text import parse_llm_json_object

log = get_logger(__name__)


async def run_resume_build_agent(
    client: AsyncOpenAI,
    settings: Settings,
    *,
    profile_notes: str,
    job_description: str | None,
) -> tuple[ResumeContentV1, list[str]]:
    steps: list[str] = []

    log.info("AI agent step: extract_facts")
    facts_resp = await client.chat.completions.create(
        model=settings.LLM_MODEL,
        max_tokens=min(2048, settings.AI_AGENT_MAX_COMPLETION_TOKENS),
        messages=[
            {"role": "system", "content": prompts.FACTS_SYSTEM},
            {
                "role": "user",
                "content": prompts.facts_user_message(profile_notes, job_description),
            },
        ],
        response_format={"type": "json_object"},
    )
    facts_raw = facts_resp.choices[0].message.content or "{}"
    facts = parse_llm_json_object(facts_raw)
    steps.append("extract_facts")

    log.info("AI agent step: synthesize_resume")
    synth_resp = await client.chat.completions.create(
        model=settings.LLM_MODEL,
        max_tokens=settings.AI_AGENT_MAX_COMPLETION_TOKENS,
        messages=[
            {"role": "system", "content": prompts.RESUME_SYNTH_SYSTEM},
            {
                "role": "user",
                "content": prompts.synth_user_message(
                    json.dumps(facts, ensure_ascii=False),
                    job_description,
                ),
            },
        ],
        response_format={"type": "json_object"},
    )
    synth_raw = synth_resp.choices[0].message.content or "{}"
    resume = ResumeContentV1.model_validate(parse_llm_json_object(synth_raw))
    steps.append("synthesize_resume")
    return resume, steps

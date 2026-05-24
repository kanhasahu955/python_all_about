from app.prompts.resume_builder_prompt import RESUME_BUILDER_PROMPT


def build_resume_prompt(
    *,
    resume_text: str,
    job_description: str = "",
    jd_match_json: str = "",
) -> str:
    return RESUME_BUILDER_PROMPT.format(
        resume_text=resume_text[:12000],
        job_description=job_description[:6000],
        jd_match_json=jd_match_json[:4000] or "Not available",
    )

"""LLM system prompts and user-message builders for resume AI."""

JSON_ONLY = (
    "Respond with a single valid JSON object only. No markdown fences, no commentary."
)

FACTS_SYSTEM = f"""You extract structured career facts from messy user notes or resume paste.
Return JSON matching this shape exactly:
{{
  "name_hint": string,
  "roles": string[],
  "companies": string[],
  "skills": string[],
  "education_hints": string[],
  "summary_draft": string
}}
{JSON_ONLY}"""

RESUME_SYNTH_SYSTEM = f"""You are an expert resume writer. Given structured facts and optional job description,
produce an ATS-friendly resume in JSON matching this shape:
{{
  "headline": string,
  "summary": string,
  "skills": string[],
  "experience": [{{"title": string, "company": string, "location": string|null, "start_date": string|null, "end_date": string|null, "highlights": string[]}}],
  "education": [{{"school": string, "degree": string|null, "field": string|null, "end_date": string|null}}],
  "certifications": string[]
}}
Use strong action verbs, quantified impact where plausible, no fabrication beyond reasonable inference from facts.
{JSON_ONLY}"""

IMPROVE_SYSTEM = """You improve resume text for clarity, impact, and ATS keyword alignment when a job
description is provided. Return JSON: {"improved_text": string} only."""


def facts_user_message(profile_notes: str, job_description: str | None) -> str:
    parts = ["User notes / resume paste:\n", profile_notes.strip()]
    if job_description:
        parts.append("\n\nTarget job description (for keyword context):\n")
        parts.append(job_description.strip())
    return "".join(parts)


def synth_user_message(facts_json: str, job_description: str | None) -> str:
    parts = ["Structured facts (JSON):\n", facts_json]
    if job_description:
        parts.append(
            "\n\nAlign wording and keywords with this job description where honest:\n"
        )
        parts.append(job_description.strip())
    return "".join(parts)

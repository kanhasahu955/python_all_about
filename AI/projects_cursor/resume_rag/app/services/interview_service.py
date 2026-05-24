import json
import re
import uuid

from sqlmodel import Session

from app.core.llm_stream import stream_chat_response
from app.repository.resume_repository import ResumeRepository
from app.services.interview_events import interview_events


INTERVIEW_PROMPT = """You are a senior technical interviewer.
Generate exactly 8 interview questions based on the candidate skills and resume below.

Return ONLY valid JSON in this exact shape:
{{
  "questions": [
    {{
      "number": 1,
      "category": "Python",
      "difficulty": "Medium",
      "question": "Clear interview question text",
      "focus": "What the interviewer is assessing"
    }}
  ]
}}

Rules:
- Mix difficulty: Easy, Medium, Hard
- Categories should match the skills provided
- Questions must be specific and practical, not generic
- No markdown fences, no extra text outside JSON

Skills:
{skills}

Resume context:
{resume_text}
"""


def _parse_questions(raw: str) -> list[dict]:
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    try:
        parsed = json.loads(text)
        questions = parsed.get("questions", [])
        if isinstance(questions, list) and questions:
            return [_normalize_question(q, i) for i, q in enumerate(questions, start=1)]
    except json.JSONDecodeError:
        pass

    lines = [line.strip("- •*").strip() for line in text.splitlines() if line.strip()]
    return [
        {
            "number": i,
            "category": "General",
            "difficulty": "Medium",
            "question": line,
            "focus": "Technical depth and communication",
        }
        for i, line in enumerate(lines[:8], start=1)
    ]


def _normalize_question(item: dict | str, index: int) -> dict:
    if isinstance(item, str):
        return {
            "number": index,
            "category": "General",
            "difficulty": "Medium",
            "question": item,
            "focus": "Technical depth and communication",
        }
    return {
        "number": item.get("number", index),
        "category": item.get("category", "General"),
        "difficulty": item.get("difficulty", "Medium"),
        "question": item.get("question", ""),
        "focus": item.get("focus", ""),
    }


def run_interview_pipeline(
    session_id: str,
    *,
    skills: str,
    document_id: str | None,
    session: Session | None,
) -> list[dict]:
    try:
        interview_events.publish_pipeline_started(session_id)

        # Step 1: load context
        interview_events.publish_agent_started(session_id, "load_context")
        resume_text = ""
        resolved_skills = skills.strip()

        if document_id and session:
            repo = ResumeRepository(session)
            doc = repo.get_by_document_id(document_id)
            if doc:
                resume_text = doc.content_text or ""
                interview_events.publish_agent_progress(
                    session_id,
                    "load_context",
                    f"Loaded resume: {doc.file_name}",
                    partial=resume_text[:400] or "No extracted text yet",
                )
                if not resolved_skills:
                    analysis = repo.get_analysis(document_id)
                    if analysis and analysis.skills_json:
                        resolved_skills = analysis.skills_json
            else:
                interview_events.publish_agent_progress(
                    session_id, "load_context", "Resume not found — using skills only"
                )

        if not resolved_skills and not resume_text:
            raise ValueError("Provide skills, a resume, or both")

        interview_events.publish_agent_completed(
            session_id,
            "load_context",
            "Context loaded",
            preview=resolved_skills[:300] if resolved_skills else resume_text[:300],
        )

        # Step 2: generate with Groq stream
        interview_events.publish_agent_started(session_id, "generate_questions")
        prompt = INTERVIEW_PROMPT.format(
            skills=resolved_skills[:3000],
            resume_text=resume_text[:4000],
        )
        raw = stream_chat_response(
            session_id,
            "generate_questions",
            prompt,
            events=interview_events,
        )
        interview_events.publish_agent_completed(
            session_id,
            "generate_questions",
            "LLM response complete",
            preview=raw[:400],
        )

        # Step 3: format
        interview_events.publish_agent_started(session_id, "format_output")
        questions = _parse_questions(raw)
        interview_events.publish_agent_completed(
            session_id,
            "format_output",
            f"Formatted {len(questions)} questions",
            questions=questions,
        )

        interview_events.publish_pipeline_completed(session_id, questions)
        return questions

    except Exception as exc:
        interview_events.publish_pipeline_failed(session_id, str(exc))
        raise


def start_interview_session(
    *,
    skills: str,
    document_id: str | None,
) -> str:
    import threading

    from app.core.database import engine

    session_id = str(uuid.uuid4())

    def _worker():
        import logging

        logger = logging.getLogger(__name__)
        try:
            with Session(engine) as db_session:
                run_interview_pipeline(
                    session_id,
                    skills=skills,
                    document_id=document_id,
                    session=db_session,
                )
        except Exception:
            logger.exception("Interview pipeline failed for session %s", session_id)

    threading.Thread(target=_worker, daemon=True).start()
    return session_id

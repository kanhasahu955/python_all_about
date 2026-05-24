import json
from datetime import datetime, timezone
from typing import Any

from app.core.redis_client import get_redis

TERMINAL_EVENTS = {"pipeline.completed", "pipeline.failed"}

INTERVIEW_LABELS: dict[str, str] = {
    "load_context": "Context Loader",
    "generate_questions": "Question Generator",
    "format_output": "Response Formatter",
}

INTERVIEW_MESSAGES: dict[str, tuple[str, str]] = {
    "load_context": ("Loading skills and resume context…", "Context ready"),
    "generate_questions": ("Generating questions with Groq…", "Raw response generated"),
    "format_output": ("Parsing and formatting questions…", "Questions formatted"),
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def buffer_key(session_id: str) -> str:
    return f"interview:buffer:{session_id}"


def channel_key(session_id: str) -> str:
    return f"interview:{session_id}"


class InterviewEventPublisher:
    def _emit(self, session_id: str, payload: dict[str, Any], *, buffer: bool = True) -> None:
        payload.setdefault("session_id", session_id)
        payload.setdefault("timestamp", _now())
        raw = json.dumps(payload, default=str)

        try:
            client = get_redis()
            if buffer:
                client.lpush(buffer_key(session_id), raw)
                client.ltrim(buffer_key(session_id), 0, 199)
                client.expire(buffer_key(session_id), 3600)
            client.publish(channel_key(session_id), raw)
        except Exception:
            pass

    def get_buffer(self, session_id: str) -> list[dict[str, Any]]:
        try:
            client = get_redis()
            rows = client.lrange(buffer_key(session_id), 0, -1)
            events = []
            for row in reversed(rows):
                if isinstance(row, bytes):
                    row = row.decode()
                events.append(json.loads(row))
            return events
        except Exception:
            return []

    def publish_pipeline_started(self, session_id: str) -> None:
        self._emit(
            session_id,
            {
                "event": "pipeline.started",
                "status": "running",
                "message": "Starting interview question pipeline…",
            },
        )

    def publish_agent_started(self, session_id: str, agent: str) -> None:
        start_msg, _ = INTERVIEW_MESSAGES.get(agent, ("Running…", "Done"))
        self._emit(
            session_id,
            {
                "event": "agent.started",
                "agent": agent,
                "label": INTERVIEW_LABELS.get(agent, agent),
                "status": "running",
                "message": start_msg,
                "partial": "",
            },
        )

    def publish_agent_token(self, session_id: str, agent: str, *, delta: str, partial: str) -> None:
        self._emit(
            session_id,
            {
                "event": "agent.token",
                "agent": agent,
                "label": INTERVIEW_LABELS.get(agent, agent),
                "status": "running",
                "token": delta,
                "partial": partial,
                "message": "Generating…",
            },
            buffer=False,
        )

    def publish_agent_progress(
        self, session_id: str, agent: str, message: str, *, partial: str | None = None
    ) -> None:
        payload: dict[str, Any] = {
            "event": "agent.progress",
            "agent": agent,
            "label": INTERVIEW_LABELS.get(agent, agent),
            "status": "running",
            "message": message,
        }
        if partial is not None:
            payload["partial"] = partial
        self._emit(session_id, payload, buffer=False)

    def publish_agent_completed(self, session_id: str, agent: str, message: str, **extra) -> None:
        payload: dict[str, Any] = {
            "event": "agent.completed",
            "agent": agent,
            "label": INTERVIEW_LABELS.get(agent, agent),
            "status": "completed",
            "message": message,
        }
        payload.update(extra)
        self._emit(session_id, payload)

    def publish_pipeline_completed(self, session_id: str, questions: list[dict]) -> None:
        self._emit(
            session_id,
            {
                "event": "pipeline.completed",
                "status": "completed",
                "message": f"Generated {len(questions)} interview questions",
                "questions": questions,
            },
        )

    def publish_pipeline_failed(self, session_id: str, error: str) -> None:
        self._emit(
            session_id,
            {
                "event": "pipeline.failed",
                "status": "failed",
                "message": error,
            },
        )


interview_events = InterviewEventPublisher()

import json
from datetime import datetime, timezone
from typing import Any

from app.core.redis_client import get_redis

TERMINAL_EVENTS = {"pipeline.completed", "pipeline.failed"}

AGENT_LABELS: dict[str, str] = {
    "parse_resume": "Resume Parser",
    "extract_skills": "Skill Extractor",
    "rag_search": "RAG Search",
    "match_jd": "JD Matcher",
    "build_resume": "Resume Builder",
}

AGENT_MESSAGES: dict[str, tuple[str, str]] = {
    "parse_resume": ("Reading PDF and extracting text…", "Resume text extracted"),
    "extract_skills": ("Analyzing skills with Groq…", "Skills and experience extracted"),
    "rag_search": ("Searching similar resumes in Pinecone…", "Context retrieved from vector store"),
    "match_jd": ("Matching resume against job description…", "Job description match scored"),
    "build_resume": ("Generating optimized resume…", "Optimized resume ready"),
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def buffer_key(document_id: str) -> str:
    return f"analysis:buffer:{document_id}"


def channel_key(document_id: str) -> str:
    return f"analysis:{document_id}"


def _preview_output(agent: str, output: dict[str, Any]) -> str | None:
    if agent == "parse_resume" and output.get("resume_text"):
        text = output["resume_text"]
        return text[:280] + ("…" if len(text) > 280 else "")
    if agent == "extract_skills" and output.get("skills_json"):
        return str(output["skills_json"])[:280]
    if agent == "match_jd":
        val = output.get("jd_match_json")
        if val:
            return str(val)[:280]
    if agent == "build_resume" and output.get("optimized_resume"):
        text = output["optimized_resume"]
        return text[:280] + ("…" if len(text) > 280 else "")
    return None


class AgentEventPublisher:
    def _emit(self, document_id: str, payload: dict[str, Any], *, buffer: bool = True) -> None:
        payload.setdefault("document_id", document_id)
        payload.setdefault("timestamp", _now())
        raw = json.dumps(payload, default=str)

        try:
            client = get_redis()
            if buffer:
                client.lpush(buffer_key(document_id), raw)
                client.ltrim(buffer_key(document_id), 0, 199)
                client.expire(buffer_key(document_id), 3600)
            client.publish(channel_key(document_id), raw)
        except Exception:
            pass

    def get_buffer(self, document_id: str) -> list[dict[str, Any]]:
        try:
            client = get_redis()
            rows = client.lrange(buffer_key(document_id), 0, -1)
            events = []
            for row in reversed(rows):
                if isinstance(row, bytes):
                    row = row.decode()
                events.append(json.loads(row))
            return events
        except Exception:
            return []

    def publish_pipeline_started(self, document_id: str, *, file_name: str | None = None) -> None:
        self._emit(
            document_id,
            {
                "event": "pipeline.started",
                "status": "running",
                "message": "Starting agent pipeline…",
                "file_name": file_name,
            },
        )

    def publish_agent_started(self, document_id: str, agent: str) -> None:
        start_msg, _ = AGENT_MESSAGES.get(agent, ("Running agent…", "Done"))
        self._emit(
            document_id,
            {
                "event": "agent.started",
                "agent": agent,
                "label": AGENT_LABELS.get(agent, agent),
                "status": "running",
                "message": start_msg,
                "partial": "",
            },
        )

    def publish_agent_token(
        self,
        document_id: str,
        agent: str,
        *,
        delta: str,
        partial: str,
    ) -> None:
        self._emit(
            document_id,
            {
                "event": "agent.token",
                "agent": agent,
                "label": AGENT_LABELS.get(agent, agent),
                "status": "running",
                "token": delta,
                "partial": partial,
                "message": "Generating…",
            },
            buffer=False,
        )

    def publish_agent_progress(
        self,
        document_id: str,
        agent: str,
        message: str,
        *,
        partial: str | None = None,
    ) -> None:
        payload: dict[str, Any] = {
            "event": "agent.progress",
            "agent": agent,
            "label": AGENT_LABELS.get(agent, agent),
            "status": "running",
            "message": message,
        }
        if partial is not None:
            payload["partial"] = partial
        self._emit(document_id, payload, buffer=False)

    def publish_agent_completed(self, document_id: str, agent: str, output: dict[str, Any]) -> None:
        _, done_msg = AGENT_MESSAGES.get(agent, ("Running…", "Completed"))
        self._emit(
            document_id,
            {
                "event": "agent.completed",
                "agent": agent,
                "label": AGENT_LABELS.get(agent, agent),
                "status": "completed",
                "message": done_msg,
                "preview": _preview_output(agent, output),
            },
        )

    def publish_agent_failed(self, document_id: str, agent: str, error: str) -> None:
        self._emit(
            document_id,
            {
                "event": "agent.failed",
                "agent": agent,
                "label": AGENT_LABELS.get(agent, agent),
                "status": "failed",
                "message": error,
            },
        )

    def publish_pipeline_completed(self, document_id: str) -> None:
        self._emit(
            document_id,
            {
                "event": "pipeline.completed",
                "status": "completed",
                "message": "All agents finished successfully",
            },
        )

    def publish_pipeline_failed(self, document_id: str, error: str) -> None:
        self._emit(
            document_id,
            {
                "event": "pipeline.failed",
                "status": "failed",
                "message": error,
            },
        )

    def publish_rag_indexed(self, document_id: str) -> None:
        self._emit(
            document_id,
            {
                "event": "rag.indexed",
                "agent": "rag_index",
                "label": "Vector Index",
                "status": "completed",
                "message": "Resume indexed in Pinecone",
            },
        )


agent_events = AgentEventPublisher()

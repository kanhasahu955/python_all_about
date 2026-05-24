import time
from typing import Protocol


class TokenEventPublisher(Protocol):
    def publish_agent_token(
        self, session_id: str, agent: str, *, delta: str, partial: str
    ) -> None: ...


def stream_chat_response(
    session_id: str | None,
    agent: str,
    prompt: str,
    *,
    char_batch: int = 18,
    interval_sec: float = 0.1,
    events: TokenEventPublisher | None = None,
) -> str:
    from app.core.llm import get_chat_llm, llm_configured
    from app.services.agent_events import agent_events

    publisher = events or agent_events

    if not llm_configured():
        return ""

    llm = get_chat_llm(streaming=True)
    parts: list[str] = []
    pending = ""
    last_emit = 0.0

    for chunk in llm.stream(prompt):
        text = chunk.content if hasattr(chunk, "content") else str(chunk)
        if not text:
            continue
        parts.append(text)
        pending += text
        now = time.time()
        if session_id and (len(pending) >= char_batch or now - last_emit >= interval_sec):
            publisher.publish_agent_token(
                session_id,
                agent,
                delta=pending,
                partial="".join(parts),
            )
            pending = ""
            last_emit = now

    full = "".join(parts)

    if session_id and pending:
        publisher.publish_agent_token(session_id, agent, delta=pending, partial=full)

    return full

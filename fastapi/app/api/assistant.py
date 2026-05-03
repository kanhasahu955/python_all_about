from pydantic import BaseModel, Field

from fastapi import APIRouter, Request

from app.assistant.intents import AssistantTurn, Intent, run_turn

router = APIRouter(prefix="/assistant", tags=["assistant"])


class TextCommand(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)


class AssistantResponse(BaseModel):
    intent: Intent
    message: str
    detail: dict | None = None


def _to_response(turn: AssistantTurn) -> AssistantResponse:
    detail = dict(turn.detail) if turn.detail else None
    if detail and "intents" in detail:
        detail["intents"] = [str(i) for i in detail["intents"]]
    return AssistantResponse(intent=turn.intent, message=turn.message, detail=detail)


@router.post("/text", response_model=AssistantResponse)
async def assistant_text(body: TextCommand, request: Request) -> AssistantResponse:
    """Jarvis-style entrypoint: today you send text; later STT posts the same payload."""
    base = str(request.base_url)
    return _to_response(run_turn(body.text, base))


@router.get("/capabilities")
async def capabilities():
    return {
        "modes": ["text"],
        "planned": ["wake_word", "streaming_stt", "tts", "allowlisted_tools"],
        "intents": [str(i) for i in Intent],
        "note": "No arbitrary shell commands; only predefined handlers.",
    }

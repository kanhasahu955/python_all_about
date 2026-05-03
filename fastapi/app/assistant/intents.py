"""Jarvis-style assistant: classify user text into intents and run allowlisted handlers only."""

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum


class Intent(StrEnum):
    STREAM = "stream"
    TIME = "time"
    HEALTH = "health"
    HELP = "help"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class AssistantTurn:
    intent: Intent
    message: str
    detail: dict | None = None


def classify(text: str) -> Intent:
    t = text.lower().strip()
    if any(k in t for k in ("stream", "camera", "video", "mjpeg", "watch")):
        return Intent.STREAM
    if any(k in t for k in ("time", "clock")):
        return Intent.TIME
    if any(k in t for k in ("health", "status", "ping", "alive")):
        return Intent.HEALTH
    if any(k in t for k in ("help", "what can you do", "capabilities")):
        return Intent.HELP
    return Intent.UNKNOWN


def handle(base_url: str, intent: Intent) -> AssistantTurn:
    base = base_url.rstrip("/")
    stream = f"{base}/stream/mjpeg"
    health_url = f"{base}/health"

    match intent:
        case Intent.STREAM:
            return AssistantTurn(
                intent=intent,
                message=f"Open the camera stream in your browser: {stream}",
                detail={"stream_url": stream},
            )
        case Intent.TIME:
            now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
            return AssistantTurn(
                intent=intent,
                message=f"The server time is {now}.",
                detail={"utc_iso": now},
            )
        case Intent.HEALTH:
            return AssistantTurn(
                intent=intent,
                message=f"You can check API health at {health_url}.",
                detail={"health_url": health_url},
            )
        case Intent.HELP:
            return AssistantTurn(
                intent=intent,
                message=(
                    "I can help with: stream / camera / video (MJPEG link), "
                    "time, health, or help. "
                    "Voice and advanced actions can be added behind the same intent router."
                ),
                detail={"intents": list(Intent)},
            )
        case _:
            return AssistantTurn(
                intent=Intent.UNKNOWN,
                message=(
                    "I did not understand that. Say help for things I can do. "
                    "(Voice recognition would send transcribed text here.)"
                ),
                detail=None,
            )


def run_turn(text: str, base_url: str) -> AssistantTurn:
    intent = classify(text)
    return handle(base_url, intent)

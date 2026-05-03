from dataclasses import dataclass
import os


def _env_int(key: str, default: int) -> int:
    raw = os.environ.get(key)
    if raw is None or raw == "":
        return default
    return int(raw)


@dataclass(frozen=True)
class Settings:
    camera_index: int = _env_int("CAMERA_INDEX", 0)
    frame_width: int = _env_int("FRAME_WIDTH", 640)
    frame_height: int = _env_int("FRAME_HEIGHT", 480)
    capture_fps_cap: int = _env_int("CAPTURE_FPS_CAP", 30)
    raw_queue_maxsize: int = _env_int("RAW_QUEUE_MAXSIZE", 2)
    host: str = os.environ.get("STREAM_HOST", "127.0.0.1")
    port: int = _env_int("STREAM_PORT", 8000)
    jpeg_quality: int = _env_int("JPEG_QUALITY", 85)


settings = Settings()

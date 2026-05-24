import asyncio
import json
import threading
from collections.abc import AsyncGenerator

from sqlmodel import Session

from app.core.database import engine
from app.core.redis_client import get_redis
from app.services.resume_service import ResumeService


def _dashboard_snapshot() -> dict:
    with Session(engine) as session:
        docs = ResumeService(session).list_resumes()

    resumes = [
        {
            "document_id": d.document_id,
            "file_name": d.file_name,
            "status": d.status.value if hasattr(d.status, "value") else d.status,
        }
        for d in docs
    ]

    analyzed = sum(1 for r in resumes if r["status"] == "analyzed")
    queued = sum(1 for r in resumes if r["status"] in ("queued", "processing"))
    failed = sum(1 for r in resumes if r["status"] == "failed")

    return {
        "event": "snapshot",
        "resumes": resumes,
        "counts": {
            "total": len(resumes),
            "analyzed": analyzed,
            "queued": queued,
            "failed": failed,
        },
    }


async def dashboard_event_stream(
    *,
    poll_interval: float = 3.0,
) -> AsyncGenerator[str, None]:
    queue: asyncio.Queue[str | None] = asyncio.Queue()
    loop = asyncio.get_running_loop()

    def _listen():
        try:
            client = get_redis()
            pubsub = client.pubsub()
            pubsub.psubscribe("analysis:*")
            for message in pubsub.listen():
                if message["type"] not in {"pmessage", "message"}:
                    continue
                asyncio.run_coroutine_threadsafe(queue.put("refresh"), loop)
        except Exception:
            pass
        finally:
            asyncio.run_coroutine_threadsafe(queue.put(None), loop)

    threading.Thread(target=_listen, daemon=True).start()

    while True:
        yield f"data: {json.dumps(_dashboard_snapshot(), default=str)}\n\n"

        try:
            signal = await asyncio.wait_for(queue.get(), timeout=poll_interval)
        except asyncio.TimeoutError:
            continue
        except asyncio.CancelledError:
            break

        if signal is None:
            break

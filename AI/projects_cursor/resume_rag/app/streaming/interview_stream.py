import asyncio
import json
import threading
from collections.abc import AsyncGenerator

from app.core.redis_client import get_redis
from app.services.interview_events import TERMINAL_EVENTS, interview_events, buffer_key, channel_key


async def interview_event_stream(session_id: str) -> AsyncGenerator[str, None]:
    for event in interview_events.get_buffer(session_id):
        yield f"data: {json.dumps(event, default=str)}\n\n"
        if event.get("event") in TERMINAL_EVENTS:
            return

    queue: asyncio.Queue[str | None] = asyncio.Queue()
    loop = asyncio.get_running_loop()

    def _listen():
        try:
            client = get_redis()
            pubsub = client.pubsub()
            pubsub.subscribe(channel_key(session_id))
            for message in pubsub.listen():
                if message["type"] != "message":
                    continue
                data = message["data"]
                if isinstance(data, bytes):
                    data = data.decode()
                asyncio.run_coroutine_threadsafe(queue.put(data), loop).result(timeout=5)
                try:
                    event = json.loads(data)
                    if event.get("event") in TERMINAL_EVENTS:
                        break
                except json.JSONDecodeError:
                    pass
            pubsub.close()
        except Exception:
            pass
        finally:
            asyncio.run_coroutine_threadsafe(queue.put(None), loop)

    threading.Thread(target=_listen, daemon=True).start()

    idle_ticks = 0
    while True:
        try:
            data = await asyncio.wait_for(queue.get(), timeout=15)
        except asyncio.TimeoutError:
            idle_ticks += 1
            yield f"data: {json.dumps({'event': 'ping', 'session_id': session_id})}\n\n"
            if idle_ticks >= 40:
                break
            continue

        if data is None:
            break

        yield f"data: {data}\n\n"
        try:
            event = json.loads(data)
            if event.get("event") in TERMINAL_EVENTS:
                break
        except json.JSONDecodeError:
            pass

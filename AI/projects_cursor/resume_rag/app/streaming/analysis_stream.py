import asyncio
import json
import threading
from collections.abc import AsyncGenerator

from app.core.redis_client import get_redis
from app.services.agent_events import TERMINAL_EVENTS, agent_events, buffer_key, channel_key


async def analysis_event_stream(document_id: str) -> AsyncGenerator[str, None]:
    for event in agent_events.get_buffer(document_id):
        yield f"data: {json.dumps(event, default=str)}\n\n"
        if event.get("event") in TERMINAL_EVENTS:
            return

    queue: asyncio.Queue[str | None] = asyncio.Queue()
    loop = asyncio.get_running_loop()

    def _listen():
        try:
            client = get_redis()
            pubsub = client.pubsub()
            pubsub.subscribe(channel_key(document_id))
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
            yield f"data: {json.dumps({'event': 'ping', 'document_id': document_id})}\n\n"
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

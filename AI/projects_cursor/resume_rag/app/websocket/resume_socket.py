import asyncio
import json
import threading

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.agent_events import TERMINAL_EVENTS as ANALYSIS_TERMINAL
from app.services.agent_events import agent_events, channel_key as analysis_channel_key
from app.services.interview_events import TERMINAL_EVENTS as INTERVIEW_TERMINAL
from app.services.interview_events import interview_events, channel_key as interview_channel_key
from app.core.redis_client import get_redis
from app.websocket.manager import manager

router = APIRouter()


async def _forward_redis_to_ws(redis_channel: str, websocket: WebSocket, terminal_events: set):
    queue: asyncio.Queue[str | None] = asyncio.Queue()
    loop = asyncio.get_running_loop()

    def _listen():
        try:
            client = get_redis()
            pubsub = client.pubsub()
            pubsub.subscribe(redis_channel)
            for message in pubsub.listen():
                if message["type"] != "message":
                    continue
                data = message["data"]
                if isinstance(data, bytes):
                    data = data.decode()
                asyncio.run_coroutine_threadsafe(queue.put(data), loop).result(timeout=5)
                try:
                    if json.loads(data).get("event") in terminal_events:
                        break
                except json.JSONDecodeError:
                    pass
            pubsub.close()
        except Exception:
            pass
        finally:
            asyncio.run_coroutine_threadsafe(queue.put(None), loop)

    threading.Thread(target=_listen, daemon=True).start()

    while True:
        data = await queue.get()
        if data is None:
            break
        try:
            await websocket.send_json(json.loads(data))
        except Exception:
            break
        try:
            if json.loads(data).get("event") in terminal_events:
                break
        except json.JSONDecodeError:
            pass


async def _replay_and_forward(
    websocket: WebSocket,
    room: str,
    buffer_events: list,
    redis_channel: str,
    terminal_events: set,
):
    await manager.connect(websocket, room)

    for event in buffer_events:
        try:
            await websocket.send_json(event)
        except Exception:
            manager.disconnect(websocket, room)
            return
        if event.get("event") in terminal_events:
            try:
                while True:
                    await websocket.receive_text()
            except WebSocketDisconnect:
                pass
            manager.disconnect(websocket, room)
            return

    forward_task = asyncio.create_task(
        _forward_redis_to_ws(redis_channel, websocket, terminal_events)
    )

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        forward_task.cancel()
        manager.disconnect(websocket, room)


@router.websocket("/ws/analysis/{document_id}")
async def analysis_socket(websocket: WebSocket, document_id: str):
    await _replay_and_forward(
        websocket,
        document_id,
        agent_events.get_buffer(document_id),
        analysis_channel_key(document_id),
        ANALYSIS_TERMINAL,
    )


@router.websocket("/ws/interview/{session_id}")
async def interview_socket(websocket: WebSocket, session_id: str):
    await _replay_and_forward(
        websocket,
        f"interview-{session_id}",
        interview_events.get_buffer(session_id),
        interview_channel_key(session_id),
        INTERVIEW_TERMINAL,
    )


@router.websocket("/ws/resume")
async def resume_socket(websocket: WebSocket):
    await manager.connect(websocket, "global")
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, "global")

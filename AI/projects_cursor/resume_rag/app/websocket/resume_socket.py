from fastapi import APIRouter
from fastapi import WebSocket

from app.websocket.manager import manager

router = APIRouter()


@router.websocket(
    "/ws/resume"
)
async def resume_socket(
    websocket: WebSocket
):

    await manager.connect(
        websocket
    )

    try:

        while True:

            await websocket.receive_text()

    except Exception:

        manager.disconnect(
            websocket
        )
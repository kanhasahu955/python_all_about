import asyncio
from typing import AsyncIterator, Optional

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

router = APIRouter(tags=["stream"])

_BOUNDARY = b"frame"


@router.get("/stream/mjpeg")
async def mjpeg_stream(request: Request) -> StreamingResponse:
    async def gen() -> AsyncIterator[bytes]:
        last_sent: Optional[bytes] = None
        while True:
            if await request.is_disconnected():
                break
            lock = request.app.state.latest_jpeg_lock
            with lock:
                chunk = request.app.state.latest_jpeg
            if chunk and chunk is not last_sent:
                last_sent = chunk
                yield (
                    b"--"
                    + _BOUNDARY
                    + b"\r\nContent-Type: image/jpeg\r\n\r\n"
                    + chunk
                    + b"\r\n"
                )
            await asyncio.sleep(1 / 30)

    return StreamingResponse(
        gen(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )

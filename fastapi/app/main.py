import asyncio
import threading
from contextlib import asynccontextmanager

import cv2
from fastapi import FastAPI

from app.api.assistant import router as assistant_router
from app.api.stream import router as stream_router
from app.pipeline.capture import CaptureThread
from app.pipeline.processor import process_frame
from app.pipeline.queue_utils import get_frame_timeout
from app.settings import settings


async def _processing_loop(capture: CaptureThread, app: FastAPI) -> None:
    jpeg_params = [cv2.IMWRITE_JPEG_QUALITY, settings.jpeg_quality]
    poll_s = 0.15
    while True:
        frame = await asyncio.to_thread(
            get_frame_timeout,
            capture.raw_queue,
            poll_s,
        )
        if frame is None:
            continue

        processed = await asyncio.to_thread(process_frame, frame)
        ok, buf = await asyncio.to_thread(
            cv2.imencode,
            ".jpg",
            processed,
            jpeg_params,
        )
        if not ok:
            continue
        blob = buf.tobytes()
        lock: threading.Lock = app.state.latest_jpeg_lock
        with lock:
            app.state.latest_jpeg = blob


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.latest_jpeg = None
    app.state.latest_jpeg_lock = threading.Lock()

    capture = CaptureThread(settings)
    capture.start()
    task = asyncio.create_task(_processing_loop(capture, app), name="cv-pipeline")
    try:
        yield
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        capture.stop()
        with app.state.latest_jpeg_lock:
            app.state.latest_jpeg = None


app = FastAPI(title="Stream CV MVP", lifespan=lifespan)
app.include_router(stream_router)
app.include_router(assistant_router)


@app.get("/health")
async def health():
    return {"status": "ok"}

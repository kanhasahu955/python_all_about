import queue
import threading
import time
from typing import Optional

import cv2
import numpy as np

from app.pipeline.queue_utils import get_drop_oldest_put
from app.settings import Settings


class CaptureThread:
    """Runs VideoCapture in a thread; pushes frames into a bounded queue (drop oldest when full)."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._raw_queue: queue.Queue[np.ndarray] = queue.Queue(
            maxsize=max(1, settings.raw_queue_maxsize)
        )
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None

    @property
    def raw_queue(self) -> queue.Queue[np.ndarray]:
        return self._raw_queue

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, name="capture", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=5.0)
            self._thread = None
        while True:
            try:
                self._raw_queue.get_nowait()
            except queue.Empty:
                break

    def _run(self) -> None:
        cap = cv2.VideoCapture(self._settings.camera_index)
        if not cap.isOpened():
            return
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, float(self._settings.frame_width))
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, float(self._settings.frame_height))
        cap.set(cv2.CAP_PROP_FPS, float(self._settings.capture_fps_cap))

        min_interval = 1.0 / max(1, self._settings.capture_fps_cap)
        last_t = 0.0

        try:
            while not self._stop.is_set():
                ok, frame = cap.read()
                if not ok:
                    time.sleep(0.05)
                    continue
                now = time.perf_counter()
                if now - last_t < min_interval:
                    continue
                last_t = now
                get_drop_oldest_put(self._raw_queue, frame.copy())
        finally:
            cap.release()

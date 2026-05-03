import time
from collections import deque

import cv2
import numpy as np

from app.settings import settings

_fps_times: deque[float] = deque(maxlen=30)


def process_frame(frame: np.ndarray) -> np.ndarray:
    """OpenCV pipeline hook: resize if needed, grayscale edge hint, overlay FPS."""
    now = time.perf_counter()
    _fps_times.append(now)
    fps = 0.0
    if len(_fps_times) >= 2:
        dt = _fps_times[-1] - _fps_times[0]
        if dt > 0:
            fps = (len(_fps_times) - 1) / dt

    target_w, target_h = settings.frame_width, settings.frame_height
    h, w = frame.shape[:2]
    if w != target_w or h != target_h:
        frame = cv2.resize(frame, (target_w, target_h), interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 60, 180)
    overlay = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    blended = cv2.addWeighted(frame, 0.65, overlay, 0.35, 0)

    label = f"FPS ~{fps:.1f} | workstation MVP"
    cv2.putText(
        blended,
        label,
        (12, 28),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 220, 0),
        2,
        cv2.LINE_AA,
    )
    return blended

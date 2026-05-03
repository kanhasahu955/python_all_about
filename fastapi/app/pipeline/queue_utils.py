import queue
from typing import Optional, TypeVar

import numpy as np

T = TypeVar("T")


def get_drop_oldest_put(q: queue.Queue[T], item: T) -> None:
    try:
        q.put_nowait(item)
    except queue.Full:
        try:
            q.get_nowait()
        except queue.Empty:
            pass
        try:
            q.put_nowait(item)
        except queue.Full:
            pass


def get_frame_timeout(
    q: queue.Queue[np.ndarray], timeout_s: float
) -> Optional[np.ndarray]:
    try:
        return q.get(timeout=timeout_s)
    except queue.Empty:
        return None

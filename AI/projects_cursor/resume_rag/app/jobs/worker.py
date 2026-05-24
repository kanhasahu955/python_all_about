import os
import platform

# macOS + fork() crashes RQ workers (libobjc); SimpleWorker avoids fork.
os.environ.setdefault("OBJC_DISABLE_INITIALIZE_FORK_SAFETY", "YES")

from rq import SimpleWorker, Worker

from app.core.redis_client import get_queue, get_redis

if __name__ == "__main__":
    worker_cls = SimpleWorker if platform.system() == "Darwin" else Worker
    worker = worker_cls([get_queue()], connection=get_redis())
    worker.work()

from rq import Worker, Queue
from redis import Redis
from app.core.config import settings

redis_conn = Redis.from_url(settings.REDIS_URL)

if __name__ == "__main__":
    worker = Worker([Queue("default", connection=redis_conn)])
    worker.work()
from fastapi import APIRouter
from redis import Redis
from rq.job import Job

from app.core.config import settings

router = APIRouter()
redis_conn = Redis.from_url(settings.REDIS_URL)


@router.get("/{job_id}")
def get_job(job_id: str):
    job = Job.fetch(job_id, connection=redis_conn)

    return {
        "job_id": job.id,
        "status": job.get_status(),
        "result": job.result,
        "exc_info": job.exc_info,
    }
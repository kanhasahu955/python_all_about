from fastapi import APIRouter, HTTPException
from rq.job import Job

from app.core.config import settings
from app.core.redis_client import get_redis

router = APIRouter()


@router.get("/{job_id}")
def get_job(job_id: str):
    if not settings.USE_REDIS_QUEUE:
        raise HTTPException(status_code=503, detail="Redis queue is disabled")

    try:
        job = Job.fetch(job_id, connection=get_redis())
    except Exception as exc:
        raise HTTPException(status_code=404, detail=f"Job not found: {exc}") from exc

    return {
        "job_id": job.id,
        "status": job.get_status(),
        "result": job.result,
        "exc_info": job.exc_info,
    }

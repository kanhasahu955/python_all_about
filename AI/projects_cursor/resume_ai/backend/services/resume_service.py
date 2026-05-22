from sqlmodel import Session

from model.resume import Resume
from repository.resume_repository import ResumeRepository
from schema.resume import ResumeCreate, ResumeUpdate
from worker.tasks import enqueue_resume_reindex


class ResumeService:
    """Application layer over ``ResumeRepository`` (+ worker hooks)."""

    def __init__(self, session: Session) -> None:
        self._repo = ResumeRepository(session)

    def list_page(self, *, limit: int, offset: int) -> tuple[list[Resume], int]:
        return self._repo.list_page(limit=limit, offset=offset)

    def get(self, resume_id: int) -> Resume:
        return self._repo.get(resume_id)

    def create(self, data: ResumeCreate) -> Resume:
        row = self._repo.create(data)
        enqueue_resume_reindex(row.id)
        return row

    def update(self, resume_id: int, data: ResumeUpdate) -> Resume:
        row = self._repo.update(resume_id, data)
        enqueue_resume_reindex(row.id)
        return row

    def delete(self, resume_id: int) -> None:
        self._repo.delete(resume_id)

from sqlalchemy import func
from sqlmodel import Session, col, select

from core.exceptions import NotFoundError
from model.resume import Resume
from schema.resume import ResumeCreate, ResumeUpdate


class ResumeRepository:
    """Persistence for ``Resume`` (SQLModel / SQLAlchemy)."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def count(self) -> int:
        stmt = select(func.count(col(Resume.id)))
        return int(self._session.exec(stmt).one())

    def list_page(self, *, limit: int, offset: int) -> tuple[list[Resume], int]:
        total = self.count()
        stmt = (
            select(Resume)
            .order_by(col(Resume.updated_at).desc())
            .offset(offset)
            .limit(limit)
        )
        rows = list(self._session.exec(stmt).all())
        return rows, total

    def get(self, resume_id: int) -> Resume:
        row = self._session.get(Resume, resume_id)
        if row is None:
            raise NotFoundError("Resume not found")
        return row

    def create(self, data: ResumeCreate) -> Resume:
        row = Resume(
            title=data.title,
            content=data.content or {},
            status=data.status,
            job_target=data.job_target,
        )
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return row

    def update(self, resume_id: int, data: ResumeUpdate) -> Resume:
        row = self.get(resume_id)
        if data.title is not None:
            row.title = data.title
        if data.content is not None:
            row.content = data.content
        if data.status is not None:
            row.status = data.status
        if data.job_target is not None:
            row.job_target = data.job_target
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return row

    def delete(self, resume_id: int) -> None:
        row = self._session.get(Resume, resume_id)
        if row is None:
            raise NotFoundError("Resume not found")
        self._session.delete(row)
        self._session.commit()

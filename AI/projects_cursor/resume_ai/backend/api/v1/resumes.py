from typing import Annotated

from fastapi import APIRouter, Depends, Query

from api.deps import get_resume_service
from schema.resume import PaginatedResumes, ResumeCreate, ResumeRead, ResumeUpdate
from services.resume_service import ResumeService
from utils.pagination import DEFAULT_PAGE_LIMIT, MAX_PAGE_LIMIT

router = APIRouter(tags=["resumes"])


@router.get("", response_model=PaginatedResumes)
def list_resumes(
    service: Annotated[ResumeService, Depends(get_resume_service)],
    limit: int = Query(default=DEFAULT_PAGE_LIMIT, ge=1, le=MAX_PAGE_LIMIT),
    offset: int = Query(default=0, ge=0),
) -> PaginatedResumes:
    rows, total = service.list_page(limit=limit, offset=offset)
    return PaginatedResumes(
        items=[ResumeRead.model_validate(r) for r in rows],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.post("", response_model=ResumeRead, status_code=201)
def create_resume(
    body: ResumeCreate,
    service: Annotated[ResumeService, Depends(get_resume_service)],
) -> ResumeRead:
    row = service.create(body)
    return ResumeRead.model_validate(row)


@router.get("/{resume_id}", response_model=ResumeRead)
def get_resume(
    resume_id: int,
    service: Annotated[ResumeService, Depends(get_resume_service)],
) -> ResumeRead:
    row = service.get(resume_id)
    return ResumeRead.model_validate(row)


@router.patch("/{resume_id}", response_model=ResumeRead)
def update_resume(
    resume_id: int,
    body: ResumeUpdate,
    service: Annotated[ResumeService, Depends(get_resume_service)],
) -> ResumeRead:
    row = service.update(resume_id, body)
    return ResumeRead.model_validate(row)


@router.delete("/{resume_id}", status_code=204)
def delete_resume(
    resume_id: int,
    service: Annotated[ResumeService, Depends(get_resume_service)],
) -> None:
    service.delete(resume_id)

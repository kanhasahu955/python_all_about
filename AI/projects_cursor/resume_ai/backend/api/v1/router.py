from fastapi import APIRouter

from api.v1 import ai, resumes

api_router = APIRouter()
api_router.include_router(resumes.router, prefix="/resumes")
api_router.include_router(ai.router)

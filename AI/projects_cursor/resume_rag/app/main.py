from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import create_db_and_tables

from app.routes import (
    health_route,
    resume_route,
    rag_route,
    datasource_route,
    job_route,
    stream_route,
)

from app.websocket.resume_socket import router as websocket_router
from app.events.registry import register_events


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    register_events()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_route.router, prefix="/api/v1")
app.include_router(resume_route.router, prefix="/api/v1/resumes")
app.include_router(rag_route.router, prefix="/api/v1/rag")
app.include_router(datasource_route.router, prefix="/api/v1/datasources")
app.include_router(job_route.router, prefix="/api/v1/jobs")
app.include_router(stream_route.router, prefix="/api/v1/stream")
app.include_router(websocket_router)

@app.get("/")
def root():
    return {
        "app": settings.APP_NAME,
        "status": "running",
        "db_provider": settings.DB_PROVIDER.value,
        "docs": "/docs",
    }
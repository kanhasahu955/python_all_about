from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import create_db_and_tables

# Routes
from app.routes import (
    health_routes,
    resume_routes,
    datasource_routes,
    rag_routes,
    job_routes,
)

# Events
from app.events.event_bus import event_bus
from app.events.resume_events import (
    RESUME_UPLOADED,
    RESUME_ANALYZED,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup
    """

    print("🚀 Starting Resume AI Backend...")

    # Create SQLModel Tables
    create_db_and_tables()

    # Register Event Handlers
    register_event_handlers()

    print("✅ Application Started")

    yield

    print("🛑 Application Shutdown")


app = FastAPI(
    title="Agentic Resume Analyzer",
    description="FastAPI + LangGraph + RAG + Snowflake + Langfuse",
    version="1.0.0",
    lifespan=lifespan,
)

# -------------------------------------------------------------------
# CORS
# -------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------

app.include_router(
    health_routes.router,
    prefix="/api/v1",
    tags=["Health"],
)

app.include_router(
    resume_routes.router,
    prefix="/api/v1/resumes",
    tags=["Resume"],
)

app.include_router(
    datasource_routes.router,
    prefix="/api/v1/datasources",
    tags=["Datasource"],
)

app.include_router(
    rag_routes.router,
    prefix="/api/v1/rag",
    tags=["RAG"],
)

app.include_router(
    job_routes.router,
    prefix="/api/v1/jobs",
    tags=["Jobs"],
)

# -------------------------------------------------------------------
# Events
# -------------------------------------------------------------------


def on_resume_uploaded(payload: dict):
    print(
        f"Resume Uploaded: {payload}"
    )


def on_resume_analyzed(payload: dict):
    print(
        f"Resume Analyzed: {payload}"
    )


def register_event_handlers():

    event_bus.subscribe(
        RESUME_UPLOADED,
        on_resume_uploaded,
    )

    event_bus.subscribe(
        RESUME_ANALYZED,
        on_resume_analyzed,
    )


# -------------------------------------------------------------------
# Root Endpoint
# -------------------------------------------------------------------


@app.get("/")
async def root():

    return {
        "name": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
    }


# -------------------------------------------------------------------
# Health Check
# -------------------------------------------------------------------


@app.get("/ping")
async def ping():

    return {
        "message": "pong"
    }
import logging
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.connections import log_connection_status
from app.core.database import create_db_and_tables, db_startup_error
from app.core.logging_config import setup_logging, print_startup_banner

from app.routes import (
    health_route,
    resume_route,
    rag_route,
    datasource_route,
    job_route,
    stream_route,
    agent_route,
)

from app.websocket.resume_socket import router as websocket_router
from app.events.registry import register_events

logger = logging.getLogger("app.main")

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print_startup_banner()
    app.state.db_error = None
    try:
        create_db_and_tables()
    except Exception as exc:
        app.state.db_error = str(exc)
        logger.error("[red bold]Database startup failed:[/] %s", exc)
    register_events()

    def _log_connections():
        try:
            log_connection_status(probe_live=True)
        except Exception as exc:
            logger.warning("Background connection check failed: %s", exc)

    threading.Thread(target=_log_connections, daemon=True).start()
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
app.include_router(agent_route.router, prefix="/api/v1/agents")
app.include_router(stream_route.router, prefix="/api/v1/stream")
app.include_router(websocket_router)

@app.get("/")
def root():
    return {
        "app": settings.APP_NAME,
        "status": "running",
        "db_provider": settings.DB_PROVIDER.value,
        "db_error": db_startup_error,
        "docs": "/docs",
    }

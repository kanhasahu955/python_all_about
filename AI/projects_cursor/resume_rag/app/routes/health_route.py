from fastapi import APIRouter, Query

from app.core.config import settings
from app.core.connections import get_connections_summary, log_connection_status

router = APIRouter()


@router.get("/health/live")
def health_live():
    return {"status": "ok", "app": settings.APP_NAME}


@router.get("/health/db-stats")
def health_db_stats():
    from sqlalchemy import text

    from app.core.database import engine

    stats = {
        "provider": settings.DB_PROVIDER.value,
        "database": getattr(settings, "SNOWFLAKE_DATABASE", None) or getattr(settings, "MYSQL_DB", None),
        "schema": getattr(settings, "SNOWFLAKE_SCHEMA", None) or "default",
        "tables": {},
    }

    try:
        with engine.connect() as conn:
            if settings.DB_PROVIDER.value == "snowflake":
                ctx = conn.execute(
                    text("SELECT CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_ROLE()")
                ).one()
                stats["current_database"] = ctx[0]
                stats["current_schema"] = ctx[1]
                stats["current_role"] = ctx[2]

            for table in ("RESUMEDOCUMENT", "RESUMEANALYSIS", "AGENTRUN"):
                try:
                    count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                    stats["tables"][table.lower()] = count
                except Exception as exc:
                    stats["tables"][table.lower()] = f"error: {exc}"
    except Exception as exc:
        stats["error"] = str(exc)

    return stats


@router.get("/health")
def health():
    summary = get_connections_summary(probe_live=True)
    db = next((c for c in summary["connections"] if c["name"] == "database"), None)

    return {
        "status": summary["status"],
        "app": settings.APP_NAME,
        "db_provider": settings.DB_PROVIDER.value,
        "db_connected": db["connected"] if db else False,
        "db_error": None if (db and db["connected"]) else (db["message"] if db else None),
    }


@router.get("/connections")
def connections(probe: bool = Query(default=True, description="Live probe each service")):
    return get_connections_summary(probe_live=probe)


@router.post("/connections/log")
def connections_log(probe: bool = Query(default=True)):
    log_connection_status(probe_live=probe)
    return {"logged": True, **get_connections_summary(probe_live=probe)}

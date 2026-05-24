import logging
from typing import Any

from pydantic import BaseModel

from app.core.config import settings
from app.core.database import db_startup_error, test_connection

logger = logging.getLogger(__name__)


class ConnectionStatus(BaseModel):
    name: str
    status: str  # ok | degraded | disabled | error
    configured: bool
    connected: bool
    message: str
    details: dict[str, Any] = {}


def _check_database() -> ConnectionStatus:
    name = "database"
    details = {"provider": settings.DB_PROVIDER.value}

    if settings.DB_PROVIDER.value == "snowflake":
        details.update(
            {
                "account": settings.SNOWFLAKE_ACCOUNT,
                "database": settings.SNOWFLAKE_DATABASE,
                "schema": settings.SNOWFLAKE_SCHEMA,
                "warehouse": settings.SNOWFLAKE_WAREHOUSE,
            }
        )
    elif settings.DB_PROVIDER.value == "mysql":
        details.update(
            {
                "host": settings.MYSQL_HOST,
                "port": settings.MYSQL_PORT,
                "database": settings.MYSQL_DB,
            }
        )
    elif settings.DB_PROVIDER.value == "databricks":
        details.update(
            {
                "host": settings.DATABRICKS_SERVER_HOSTNAME,
                "catalog": settings.DATABRICKS_CATALOG,
                "schema": settings.DATABRICKS_SCHEMA,
            }
        )

    ok, err = test_connection()
    if ok:
        return ConnectionStatus(
            name=name,
            status="ok",
            configured=True,
            connected=True,
            message=f"{settings.DB_PROVIDER.value} connected",
            details=details,
        )

    error = err or db_startup_error or "connection failed"
    return ConnectionStatus(
        name=name,
        status="error",
        configured=True,
        connected=False,
        message=error,
        details=details,
    )


def _check_groq() -> ConnectionStatus:
    name = "groq"
    details = {"model": settings.GROQ_MODEL}

    if not settings.GROQ_API_KEY:
        return ConnectionStatus(
            name=name,
            status="disabled",
            configured=False,
            connected=False,
            message="GROQ_API_KEY not set",
            details=details,
        )

    try:
        from langchain_groq import ChatGroq

        ChatGroq(model=settings.GROQ_MODEL, api_key=settings.GROQ_API_KEY)
        return ConnectionStatus(
            name=name,
            status="ok",
            configured=True,
            connected=True,
            message="Groq client configured",
            details=details,
        )
    except Exception as exc:
        return ConnectionStatus(
            name=name,
            status="error",
            configured=True,
            connected=False,
            message=str(exc),
            details=details,
        )


def _check_openai_embeddings() -> ConnectionStatus:
    name = "openai_embeddings"
    details = {"model": "text-embedding-3-small", "purpose": "RAG vector embeddings"}

    if not settings.OPENAI_API_KEY:
        return ConnectionStatus(
            name=name,
            status="disabled",
            configured=False,
            connected=False,
            message="OPENAI_API_KEY not set (required for RAG indexing/search)",
            details=details,
        )

    try:
        from app.rag.embeddings import get_embedding_model

        vec = get_embedding_model().embed_query("connection test")
        details["dimensions"] = len(vec)
        return ConnectionStatus(
            name=name,
            status="ok",
            configured=True,
            connected=True,
            message="OpenAI embeddings reachable",
            details=details,
        )
    except Exception as exc:
        return ConnectionStatus(
            name=name,
            status="error",
            configured=True,
            connected=False,
            message=str(exc),
            details=details,
        )


def _check_pinecone() -> ConnectionStatus:
    name = "pinecone"
    details = {
        "index": settings.PINECONE_INDEX_NAME,
        "namespace": settings.PINECONE_NAMESPACE,
        "env": settings.PINECONE_ENV,
    }

    if not settings.PINECONE_API_KEY:
        return ConnectionStatus(
            name=name,
            status="disabled",
            configured=False,
            connected=False,
            message="PINECONE_API_KEY not set",
            details=details,
        )

    try:
        from app.rag.pinecone_store import PineconeStore

        store = PineconeStore()
        index = store._get_index()
        stats = index.describe_index_stats()
        details["total_vectors"] = stats.get("total_vector_count", 0)
        namespaces = stats.get("namespaces") or {}
        ns_stats = namespaces.get(settings.PINECONE_NAMESPACE, {})
        details["namespace_vectors"] = ns_stats.get("vector_count", 0)
        return ConnectionStatus(
            name=name,
            status="ok",
            configured=True,
            connected=True,
            message="Pinecone index reachable",
            details=details,
        )
    except Exception as exc:
        return ConnectionStatus(
            name=name,
            status="error",
            configured=True,
            connected=False,
            message=str(exc),
            details=details,
        )


def _check_rag() -> ConnectionStatus:
    name = "rag"
    openai = _check_openai_embeddings()
    pinecone = _check_pinecone()

    details = {
        "openai_embeddings": openai.status,
        "pinecone": pinecone.status,
    }

    if openai.connected and pinecone.connected:
        return ConnectionStatus(
            name=name,
            status="ok",
            configured=True,
            connected=True,
            message="RAG pipeline ready (embeddings + Pinecone)",
            details=details,
        )

    if not openai.configured and not pinecone.configured:
        return ConnectionStatus(
            name=name,
            status="disabled",
            configured=False,
            connected=False,
            message="Configure OPENAI_API_KEY and PINECONE_API_KEY for RAG",
            details=details,
        )

    return ConnectionStatus(
        name=name,
        status="degraded",
        configured=True,
        connected=False,
        message="RAG partially configured — check OpenAI embeddings and Pinecone",
        details=details,
    )


def _check_redis() -> ConnectionStatus:
    name = "redis"
    details = {
        "url": settings.REDIS_URL.split("@")[-1] if "@" in settings.REDIS_URL else settings.REDIS_URL,
        "queue_enabled": settings.USE_REDIS_QUEUE,
    }

    try:
        from app.core.redis_client import ping_redis

        ping_redis()
        message = "Redis reachable"
        if settings.USE_REDIS_QUEUE:
            message += " — background queue enabled"
        else:
            message += " — queue disabled (USE_REDIS_QUEUE=false)"
        return ConnectionStatus(
            name=name,
            status="ok",
            configured=True,
            connected=True,
            message=message,
            details=details,
        )
    except Exception as exc:
        if not settings.USE_REDIS_QUEUE:
            return ConnectionStatus(
                name=name,
                status="warning",
                configured=True,
                connected=False,
                message=f"Redis unreachable (queue disabled): {exc}",
                details=details,
            )
        return ConnectionStatus(
            name=name,
            status="error",
            configured=True,
            connected=False,
            message=str(exc),
            details=details,
        )


def _check_langfuse() -> ConnectionStatus:
    name = "langfuse"
    details = {"host": settings.LANGFUSE_HOST}

    if not settings.LANGFUSE_PUBLIC_KEY or not settings.LANGFUSE_SECRET_KEY:
        return ConnectionStatus(
            name=name,
            status="disabled",
            configured=False,
            connected=False,
            message="Langfuse keys not set",
            details=details,
        )

    return ConnectionStatus(
        name=name,
        status="ok",
        configured=True,
        connected=True,
        message="Langfuse configured",
        details=details,
    )


def get_all_connection_statuses(*, probe_live: bool = True) -> list[ConnectionStatus]:
    checks = [
        _check_database(),
        _check_groq(),
        _check_langfuse(),
    ]
    if probe_live:
        openai = _check_openai_embeddings()
        pinecone = _check_pinecone()
        checks.extend([openai, pinecone, _check_rag(), _check_redis()])
    else:
        checks.extend([
            ConnectionStatus(name="openai_embeddings", status="unknown", configured=bool(settings.OPENAI_API_KEY), connected=False, message="probe disabled"),
            ConnectionStatus(name="pinecone", status="unknown", configured=bool(settings.PINECONE_API_KEY), connected=False, message="probe disabled"),
            ConnectionStatus(name="rag", status="unknown", configured=False, connected=False, message="probe disabled"),
            ConnectionStatus(name="redis", status="unknown", configured=settings.USE_REDIS_QUEUE, connected=False, message="probe disabled"),
        ])
    return checks


def get_connections_summary(probe_live: bool = True) -> dict[str, Any]:
    statuses = get_all_connection_statuses(probe_live=probe_live)
    overall = "ok"
    if any(s.status == "error" for s in statuses):
        overall = "degraded"
    elif all(s.status == "disabled" for s in statuses):
        overall = "disabled"

    return {
        "status": overall,
        "app": settings.APP_NAME,
        "connections": [s.model_dump() for s in statuses],
    }


def log_connection_status(probe_live: bool = True) -> None:
    from app.core.logging_config import log_connection_status_structured, print_connection_banner

    summary = get_connections_summary(probe_live=probe_live)
    print_connection_banner(summary)
    log_connection_status_structured(summary)


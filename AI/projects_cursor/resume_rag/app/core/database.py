from sqlalchemy import create_engine, text
from sqlmodel import SQLModel, Session

from app.core.config import DBProvider, settings
from app.core.db_url import (
    build_mysql_admin_url,
    build_snowflake_bootstrap_url,
    snowflake_connect_args,
)

db_startup_error: str | None = None

_engine_kwargs: dict = {
    "echo": False,
    "pool_pre_ping": True,
}

if settings.DB_PROVIDER == DBProvider.snowflake:
    _engine_kwargs["connect_args"] = snowflake_connect_args(settings)

_TEXT_COLUMNS = {
    "resumedocument": ["content_text"],
    "resumeanalysis": [
        "skills_json",
        "jd_match_json",
        "optimized_resume",
        "interview_questions",
        "evaluation_json",
    ],
    "backgroundjob": ["result_json", "error"],
}


def _ensure_mysql_database():
    if settings.DB_PROVIDER != DBProvider.mysql:
        return

    admin_engine = create_engine(
        build_mysql_admin_url(settings),
        isolation_level="AUTOCOMMIT",
    )
    with admin_engine.connect() as conn:
        conn.execute(
            text(f"CREATE DATABASE IF NOT EXISTS `{settings.MYSQL_DB}`")
        )
    admin_engine.dispose()


def _ensure_snowflake_objects():
    if settings.DB_PROVIDER != DBProvider.snowflake:
        return

    bootstrap_engine = create_engine(
        build_snowflake_bootstrap_url(settings),
        connect_args=snowflake_connect_args(settings),
    )
    db = settings.SNOWFLAKE_DATABASE
    schema = settings.SNOWFLAKE_SCHEMA

    with bootstrap_engine.connect() as conn:
        conn.execute(text(f'CREATE DATABASE IF NOT EXISTS "{db}"'))
        conn.execute(text(f'USE DATABASE "{db}"'))
        conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))
        conn.execute(text(f'USE SCHEMA "{schema}"'))
        conn.commit()
    bootstrap_engine.dispose()


def _upgrade_text_columns():
    if settings.DB_PROVIDER != DBProvider.mysql:
        return

    with engine.connect() as conn:
        for table, columns in _TEXT_COLUMNS.items():
            for column in columns:
                conn.execute(
                    text(f"ALTER TABLE `{table}` MODIFY COLUMN `{column}` TEXT")
                )
        conn.commit()


_ensure_mysql_database()

engine = create_engine(settings.DATABASE_URL, **_engine_kwargs)


def test_connection() -> tuple[bool, str | None]:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True, None
    except Exception as exc:
        return False, str(exc)


def _snowflake_table_columns(conn, schema: str, table: str) -> set[str]:
    db = (settings.SNOWFLAKE_DATABASE or "").upper()
    try:
        rows = conn.execute(
            text(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_catalog = :db
                  AND table_schema = :schema
                  AND table_name = :table
                """
            ),
            {"db": db, "schema": schema, "table": table.upper()},
        ).fetchall()
        return {str(row[0]).upper() for row in rows}
    except Exception:
        return set()


def _migrate_snowflake_resume_schema():
    """Recreate resume tables only when legacy auto-increment ID schema is detected."""
    if settings.DB_PROVIDER != DBProvider.snowflake:
        return

    schema = (settings.SNOWFLAKE_SCHEMA or "PUBLIC").upper()
    with engine.connect() as conn:
        doc_cols = _snowflake_table_columns(conn, schema, "RESUMEDOCUMENT")

        # No table yet — create_all will handle it. Never drop on uncertainty.
        if not doc_cols:
            return

        # Already on UUID/document_id primary key schema.
        if "DOCUMENT_ID" in doc_cols and "ID" not in doc_cols:
            return

        # Legacy schema with integer ID — recreate resume tables once.
        for table in ("AGENTRUN", "RESUMEANALYSIS", "RESUMEDOCUMENT"):
            try:
                conn.execute(text(f'DROP TABLE IF EXISTS "{schema}"."{table}"'))
            except Exception:
                pass
        conn.commit()


def create_db_and_tables():
    global db_startup_error

    from app.models.agent_model import AgentRun  # noqa: F401
    from app.models.datasource_model import DataSource  # noqa: F401
    from app.models.job_model import BackgroundJob  # noqa: F401
    from app.models.resume_model import ResumeAnalysis, ResumeDocument  # noqa: F401

    ok, err = test_connection()
    if not ok:
        db_startup_error = err
        raise RuntimeError(err)

    if settings.DB_PROVIDER == DBProvider.snowflake:
        _ensure_snowflake_objects()
        _migrate_snowflake_resume_schema()
        for table in SQLModel.metadata.sorted_tables:
            table.indexes.clear()

    SQLModel.metadata.create_all(engine)
    db_startup_error = None

    try:
        _ensure_optional_columns()
    except Exception:
        pass

    try:
        _upgrade_text_columns()
    except Exception:
        pass


def _ensure_optional_columns():
    """Add columns introduced after initial deploy (Snowflake / MySQL)."""
    with engine.connect() as conn:
        if settings.DB_PROVIDER == DBProvider.snowflake:
            schema = (settings.SNOWFLAKE_SCHEMA or "PUBLIC").upper()
            cols = _snowflake_table_columns(conn, schema, "RESUMEDOCUMENT")
            if cols and "JOB_ID" not in cols:
                conn.execute(text('ALTER TABLE "RESUMEDOCUMENT" ADD COLUMN JOB_ID VARCHAR'))
                conn.commit()
        elif settings.DB_PROVIDER == DBProvider.mysql:
            try:
                conn.execute(
                    text(
                        "ALTER TABLE `resumedocument` "
                        "ADD COLUMN IF NOT EXISTS `job_id` VARCHAR(255) NULL"
                    )
                )
                conn.commit()
            except Exception:
                pass


def get_session():
    with Session(engine) as session:
        yield session

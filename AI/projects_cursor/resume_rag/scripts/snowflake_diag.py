"""Diagnose Snowflake tables and data using ORM models (no raw SQL)."""
from sqlalchemy import func, inspect
from sqlmodel import Session, select

from app.core.config import settings
from app.core.database import create_db_and_tables, engine, test_connection
from app.models.agent_model import AgentRun
from app.models.datasource_model import DataSource
from app.models.job_model import BackgroundJob
from app.models.resume_model import ResumeAnalysis, ResumeDocument
from app.repository.resume_repository import ResumeRepository

# ORM models registered in the app schema
DIAG_MODELS: list[tuple[str, type]] = [
    ("AgentRun", AgentRun),
    ("BackgroundJob", BackgroundJob),
    ("DataSource", DataSource),
    ("ResumeAnalysis", ResumeAnalysis),
    ("ResumeDocument", ResumeDocument),
]


def _resolve_table_name(inspector, model: type) -> str | None:
    """Map SQLModel __tablename__ to the name Snowflake actually uses."""
    expected = model.__tablename__
    names = {name.lower(): name for name in inspector.get_table_names()}
    return names.get(expected.lower())


def _count_rows(session: Session, model: type) -> int:
    return session.exec(select(func.count()).select_from(model)).one()


def _resume_document_schema(inspector) -> dict:
    table = _resolve_table_name(inspector, ResumeDocument)
    if not table:
        return {
            "table_exists": False,
            "column_names": [],
            "primary_key": [],
            "legacy_id_column": False,
            "document_id_column": False,
        }

    columns = inspector.get_columns(table)
    column_names = [col["name"].upper() for col in columns]
    pk_info = inspector.get_pk_constraint(table) or {}
    pk_columns = [col.upper() for col in pk_info.get("constrained_columns", [])]

    return {
        "table_exists": True,
        "table_name": table,
        "column_names": column_names,
        "primary_key": pk_columns,
        "legacy_id_column": "ID" in column_names,
        "document_id_column": "DOCUMENT_ID" in column_names,
    }


def main():
    print(f"Database: {settings.SNOWFLAKE_DATABASE}")
    print(f"Schema:   {settings.SNOWFLAKE_SCHEMA}")
    print(f"Account:  {settings.SNOWFLAKE_ACCOUNT}")
    print(f"Provider: {settings.DB_PROVIDER.value}")
    print()

    ok, err = test_connection()
    if not ok:
        print(f"Connection failed: {err}")
        return

    print(
        f"Connected (configured): db={settings.SNOWFLAKE_DATABASE} "
        f"schema={settings.SNOWFLAKE_SCHEMA}"
    )
    print()

    inspector = inspect(engine)
    schema_info = _resume_document_schema(inspector)

    print("ORM table row counts:")
    with Session(engine) as session:
        for label, model in DIAG_MODELS:
            try:
                live_count = _count_rows(session, model)
            except Exception as exc:
                live_count = f"error: {exc}"
            print(f"  {label:20} {live_count}")

    print()
    if schema_info["table_exists"]:
        print(f"ResumeDocument table: {schema_info['table_name']}")
        print(f"  Primary key (ORM inspect): {schema_info['primary_key']}")
        print(f"  Has DOCUMENT_ID column: {schema_info['document_id_column']}")
        print(f"  Has legacy ID column:     {schema_info['legacy_id_column']}")
        key_cols = [
            name
            for name in ("DOCUMENT_ID", "ID")
            if name in schema_info["column_names"]
        ]
        print(f"  Key columns present:      {key_cols}")
    else:
        print("ResumeDocument table not found — create_db_and_tables() will create it.")

    print("\nRunning create_db_and_tables() (simulates app restart)...")
    create_db_and_tables()

    with Session(engine) as session:
        row_count = _count_rows(session, ResumeDocument)
        docs = ResumeRepository(session).list_documents()
        print(f"ResumeDocument rows after startup: {row_count}")
        if docs:
            print("  Latest:")
            for doc in docs[:5]:
                status = doc.status.value if hasattr(doc.status, "value") else doc.status
                print(f"    {doc.document_id[:8]}…  {doc.file_name}  ({status})")

    if row_count == 0:
        print("\nNOTE: If you expected rows, re-upload resumes after fixing migration.")
    else:
        print("\nOK: Data survived app startup migration.")


if __name__ == "__main__":
    main()

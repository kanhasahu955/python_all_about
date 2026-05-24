"""Diagnose Snowflake tables and data."""
from sqlalchemy import text

from app.core.config import settings
from app.core.database import create_db_and_tables, engine


def main():
    schema = (settings.SNOWFLAKE_SCHEMA or "PUBLIC").upper()
    db = (settings.SNOWFLAKE_DATABASE or "").upper()

    print(f"Database: {db}")
    print(f"Schema:   {schema}")
    print(f"Account:  {settings.SNOWFLAKE_ACCOUNT}")
    print()

    with engine.connect() as conn:
        ctx = conn.execute(
            text("SELECT CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_ROLE()")
        ).one()
        print(f"Connected as: db={ctx[0]} schema={ctx[1]} role={ctx[2]}")
        print()

        tables = conn.execute(
            text(
                """
                SELECT table_name, row_count
                FROM information_schema.tables
                WHERE table_catalog = :db AND table_schema = :schema
                ORDER BY table_name
                """
            ),
            {"db": db, "schema": schema},
        ).fetchall()

        print("Tables:")
        for name, row_count in tables:
            try:
                live = conn.execute(text(f'SELECT COUNT(*) FROM "{name}"')).scalar()
            except Exception as exc:
                live = f"error: {exc}"
            print(f"  {name:20} metadata_rows={row_count}  live_count={live}")

        doc_cols = conn.execute(
            text(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_catalog = :db
                  AND table_schema = :schema
                  AND table_name = 'RESUMEDOCUMENT'
                  AND column_name IN ('ID', 'DOCUMENT_ID')
                ORDER BY column_name
                """
            ),
            {"db": db, "schema": schema},
        ).fetchall()
        print()
        print(f"RESUMEDOCUMENT key columns present: {[c[0] for c in doc_cols]}")

    print("\nRunning create_db_and_tables() (simulates app restart)...")
    create_db_and_tables()

    with engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM RESUMEDOCUMENT")).scalar()
        print(f"RESUMEDOCUMENT rows after startup: {count}")
        if count == 0:
            print("\nNOTE: If you expected rows, re-upload resumes after fixing migration.")
        else:
            print("\nOK: Data survived app startup migration.")


if __name__ == "__main__":
    main()

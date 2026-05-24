from urllib.parse import quote_plus

from sqlalchemy import create_engine, text

from app.schemas.datasource_schema import DataSourceCreate, DataSourceTestRequest


def build_datasource_url(payload: DataSourceCreate | DataSourceTestRequest) -> str:
    provider = payload.provider.lower()
    username = quote_plus(payload.username or "")
    password = quote_plus(payload.password or "")

    if provider == "mysql":
        port = payload.port or 3306
        db = payload.database_name or ""
        return f"mysql+pymysql://{username}:{password}@{payload.host}:{port}/{db}"

    if provider in {"postgres", "postgresql"}:
        port = payload.port or 5432
        db = payload.database_name or "postgres"
        return f"postgresql+psycopg2://{username}:{password}@{payload.host}:{port}/{db}"

    if provider == "snowflake":
        account = (payload.host or "").strip()
        db = payload.database_name or ""
        schema = payload.schema_name or "PUBLIC"
        warehouse = payload.warehouse or ""
        role = payload.role or ""
        params = []
        if warehouse:
            params.append(f"warehouse={warehouse}")
        if role:
            params.append(f"role={role}")
        query = f"?{'&'.join(params)}" if params else ""
        return f"snowflake://{username}:{password}@{account}/{db}/{schema}{query}"

    if provider == "databricks":
        token = quote_plus(payload.token or payload.password or "")
        host = payload.host or ""
        http_path = quote_plus(payload.http_path or "")
        catalog = payload.catalog or "main"
        schema = payload.schema_name or "default"
        return (
            f"databricks://token:{token}@{host}"
            f"?http_path={http_path}&catalog={catalog}&schema={schema}"
        )

    raise ValueError(f"Unsupported provider: {provider}")


def test_datasource_connection(payload: DataSourceTestRequest) -> dict:
    try:
        url = build_datasource_url(payload)
        engine = create_engine(url, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        engine.dispose()
        return {"success": True, "message": f"Connected to {payload.provider} successfully"}
    except Exception as exc:
        return {"success": False, "message": str(exc)}

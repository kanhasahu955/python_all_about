from urllib.parse import quote_plus

from app.core.config import DBProvider, Settings


def build_mysql_admin_url(settings: Settings) -> str:
    return (
        f"mysql+pymysql://{quote_plus(settings.MYSQL_USER)}:"
        f"{quote_plus(settings.MYSQL_PASSWORD)}@"
        f"{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/"
    )


def _snowflake_account_locator(settings: Settings) -> str:
    account = (settings.SNOWFLAKE_ACCOUNT or "").strip()
    if not account:
        return account

    # Org-style accounts (ORG-ACCOUNT) use the identifier as-is.
    # Legacy accounts need account.region.cloud — set SNOWFLAKE_LEGACY_LOCATOR=true.
    if settings.SNOWFLAKE_LEGACY_LOCATOR and settings.SNOWFLAKE_REGION:
        if settings.SNOWFLAKE_REGION not in account:
            cloud = settings.SNOWFLAKE_CLOUD or "aws"
            return f"{account}.{settings.SNOWFLAKE_REGION}.{cloud}"

    return account


def snowflake_connect_args(settings: Settings) -> dict:
    args = {"client_session_keep_alive": True}
    if settings.SNOWFLAKE_HOST:
        args["host"] = settings.SNOWFLAKE_HOST
    return args


def build_snowflake_bootstrap_url(settings: Settings) -> str:
    account = _snowflake_account_locator(settings)
    return (
        f"snowflake://{quote_plus(settings.SNOWFLAKE_USER or '')}:"
        f"{quote_plus(settings.SNOWFLAKE_PASSWORD or '')}@"
        f"{account}/?warehouse={settings.SNOWFLAKE_WAREHOUSE}&role={settings.SNOWFLAKE_ROLE}"
    )


def build_database_url(settings: Settings) -> str:
    provider = settings.DB_PROVIDER

    if provider == DBProvider.mysql:
        return (
            f"mysql+pymysql://{quote_plus(settings.MYSQL_USER)}:"
            f"{quote_plus(settings.MYSQL_PASSWORD)}@"
            f"{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/"
            f"{settings.MYSQL_DB}"
        )

    if provider == DBProvider.snowflake:
        account = _snowflake_account_locator(settings)
        return (
            f"snowflake://{quote_plus(settings.SNOWFLAKE_USER or '')}:"
            f"{quote_plus(settings.SNOWFLAKE_PASSWORD or '')}@"
            f"{account}/"
            f"{settings.SNOWFLAKE_DATABASE}/{settings.SNOWFLAKE_SCHEMA}"
            f"?warehouse={settings.SNOWFLAKE_WAREHOUSE}&role={settings.SNOWFLAKE_ROLE}"
        )

    if provider == DBProvider.databricks:
        return (
            f"databricks://token:{quote_plus(settings.DATABRICKS_ACCESS_TOKEN or '')}@"
            f"{settings.DATABRICKS_SERVER_HOSTNAME}"
            f"?http_path={quote_plus(settings.DATABRICKS_HTTP_PATH or '')}"
            f"&catalog={settings.DATABRICKS_CATALOG}"
            f"&schema={settings.DATABRICKS_SCHEMA}"
        )

    raise ValueError(f"Unsupported DB_PROVIDER: {provider}")

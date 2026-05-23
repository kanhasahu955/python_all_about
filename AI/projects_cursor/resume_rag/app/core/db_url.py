from urllib.parse import quote_plus

from app.core.config import DBProvider, Settings


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
        return (
            f"snowflake://{quote_plus(settings.SNOWFLAKE_USER)}:"
            f"{quote_plus(settings.SNOWFLAKE_PASSWORD)}@"
            f"{settings.SNOWFLAKE_ACCOUNT}/"
            f"{settings.SNOWFLAKE_DATABASE}/{settings.SNOWFLAKE_SCHEMA}"
            f"?warehouse={settings.SNOWFLAKE_WAREHOUSE}&role={settings.SNOWFLAKE_ROLE}"
        )

    if provider == DBProvider.databricks:
        return (
            f"databricks://token:{quote_plus(settings.DATABRICKS_ACCESS_TOKEN)}@"
            f"{settings.DATABRICKS_SERVER_HOSTNAME}"
            f"?http_path={quote_plus(settings.DATABRICKS_HTTP_PATH)}"
            f"&catalog={settings.DATABRICKS_CATALOG}"
            f"&schema={settings.DATABRICKS_SCHEMA}"
        )

    raise ValueError(f"Unsupported DB_PROVIDER: {provider}")

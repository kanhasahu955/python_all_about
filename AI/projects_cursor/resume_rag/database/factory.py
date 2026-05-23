from database.adapters.mysql import MySQLAdapter
from database.adapters.postgres import PostgreSQLAdapter
from database.adapters.sqlserver import SQLServerAdapter
from database.adapters.snowflake import SnowflakeAdapter
from database.adapters.databricks import DatabricksAdapter
from database.adapters.bigquery import BigQueryAdapter


class AdapterFactory:
    @staticmethod
    def create(provider: str, config: dict):

        provider = provider.lower()

        adapters = {
            "mysql": MySQLAdapter,
            "postgres": PostgreSQLAdapter,
            "sqlserver": SQLServerAdapter,
            "snowflake": SnowflakeAdapter,
            "databricks": DatabricksAdapter,
            "bigquery": BigQueryAdapter,
        }

        adapter_class = adapters.get(provider)

        if not adapter_class:
            raise ValueError(f"Unsupported provider: {provider}")

        return adapter_class(config)
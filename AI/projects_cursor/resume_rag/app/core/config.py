from enum import Enum
from pathlib import Path

from pydantic import computed_field, field_validator
from pydantic_settings import BaseSettings

AI_ROOT = Path(__file__).resolve().parents[2].parent.parent
ENV_FILE = AI_ROOT / ".env"


class DBProvider(str, Enum):
    mysql = "mysql"
    snowflake = "snowflake"
    databricks = "databricks"


class Settings(BaseSettings):
    APP_NAME: str = "Agentic Resume AI"

    # mysql | snowflake | databricks  (set in AI/.env)
    DB_PROVIDER: DBProvider = DBProvider.mysql

    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "password"
    MYSQL_DB: str = "resume_ai"

    SNOWFLAKE_ACCOUNT: str | None = None
    SNOWFLAKE_USER: str | None = None
    SNOWFLAKE_PASSWORD: str | None = None
    SNOWFLAKE_DATABASE: str | None = None
    SNOWFLAKE_SCHEMA: str = "PUBLIC"
    SNOWFLAKE_WAREHOUSE: str | None = None
    SNOWFLAKE_ROLE: str | None = None

    DATABRICKS_SERVER_HOSTNAME: str | None = None
    DATABRICKS_HTTP_PATH: str | None = None
    DATABRICKS_ACCESS_TOKEN: str | None = None
    DATABRICKS_CATALOG: str = "main"
    DATABRICKS_SCHEMA: str = "default"

    REDIS_URL: str = "redis://localhost:6379/0"
    USE_REDIS_QUEUE: bool = False

    OPENAI_API_KEY: str | None = None

    PINECONE_API_KEY: str | None = None
    PINECONE_INDEX_NAME: str = "resume-ai-index"
    PINECONE_NAMESPACE: str = "resumes"

    LANGFUSE_PUBLIC_KEY: str | None = None
    LANGFUSE_SECRET_KEY: str | None = None
    LANGFUSE_HOST: str = "https://cloud.langfuse.com"

    @field_validator("DB_PROVIDER", mode="before")
    @classmethod
    def normalize_provider(cls, value):
        if isinstance(value, str):
            return value.strip().lower()
        return value

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        from app.core.db_url import build_database_url

        return build_database_url(self)

    class Config:
        env_file = str(ENV_FILE)
        extra = "ignore"


settings = Settings()

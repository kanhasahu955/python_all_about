from functools import lru_cache

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    ############################################################
    # APP
    ############################################################
    APP_NAME: str = "Resume Analyser"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173",
        description="Comma-separated origins for CORS.",
    )

    ############################################################
    # SECURITY
    ############################################################
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    ############################################################
    # DATABASE (MySQL)
    ############################################################
    MYSQL_HOST: str = Field(..., env="MYSQL_HOST")
    MYSQL_PORT: int = Field(3306, env="MYSQL_PORT")
    MYSQL_USER: str = Field(..., env="MYSQL_USER")
    MYSQL_PASSWORD: str = Field(..., env="MYSQL_PASSWORD")
    MYSQL_DB: str = Field(..., env="MYSQL_DB")


    ############################################################
    # LANGCHAIN
    ############################################################
    LANGCHAIN_TRACING_V2: bool = True
    LANGCHAIN_PROJECT: str = "resume-rag"
    LANGCHAIN_API_KEY: str | None = Field(default=None, env="LANGCHAIN_API_KEY")

    ############################################################
    # LANGGRAPH
    ############################################################
    LANGGRAPH_RECURSION_LIMIT: int = 50
    LANGGRAPH_MAX_CONCURRENCY: int = 10

    ############################################################
    # LANGFUSE
    ############################################################
    LANGFUSE_PUBLIC_KEY: str | None = Field(default=None, env="LANGFUSE_PUBLIC_KEY")
    LANGFUSE_SECRET_KEY: str | None = Field(default=None, env="LANGFUSE_SECRET_KEY")
    LANGFUSE_HOST: str = Field(
        default="https://cloud.langfuse.com",
        env="LANGFUSE_HOST",
    )

    ############################################################
    # PINECONE
    ############################################################
    PINECONE_API_KEY: str = Field(..., env="PINECONE_API_KEY")
    PINECONE_ENV: str = Field(..., env="PINECONE_ENV")
    PINECONE_INDEX_NAME: str = Field(
        default="resume-ai-index",
        env="PINECONE_INDEX_NAME",
    )
    PINECONE_NAMESPACE: str = Field(
        default="resumes",
        env="PINECONE_NAMESPACE",
    )

    ############################################################
    # LLM / EMBEDDING
    ############################################################
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    LLM_MODEL: str = "gpt-4o-mini"
    OPENAI_TIMEOUT_SECONDS: float = 120.0
    AI_AGENT_MAX_COMPLETION_TOKENS: int = 4096

    ############################################################
    # FILE STORAGE
    ############################################################
    STORAGE_TYPE: str = "local"
    STORAGE_PATH: str = "storage"

    ############################################################
    # SNOWFLAKE
    ############################################################
    SNOWFLAKE_ACCOUNT: str | None = Field(default=None, env="SNOWFLAKE_ACCOUNT")
    SNOWFLAKE_USER: str | None = Field(default=None, env="SNOWFLAKE_USER")
    SNOWFLAKE_PASSWORD: str | None = Field(default=None, env="SNOWFLAKE_PASSWORD")
    SNOWFLAKE_DATABASE: str | None = Field(default=None, env="SNOWFLAKE_DATABASE")
    SNOWFLAKE_SCHEMA: str | None = Field(default=None, env="SNOWFLAKE_SCHEMA")
    SNOWFLAKE_WAREHOUSE: str | None = Field(default=None, env="SNOWFLAKE_WAREHOUSE")
    SNOWFLAKE_ROLE: str | None = Field(default=None, env="SNOWFLAKE_ROLE")

    ############################################################
    # DATABRICKS
    ############################################################
    DATABRICKS_SERVER_HOSTNAME: str | None = Field(
        default=None,
        env="DATABRICKS_SERVER_HOSTNAME",
    )
    DATABRICKS_HTTP_PATH: str | None = Field(
        default=None,
        env="DATABRICKS_HTTP_PATH",
    )
    DATABRICKS_ACCESS_TOKEN: str | None = Field(
        default=None,
        env="DATABRICKS_ACCESS_TOKEN",
    )
    DATABRICKS_CATALOG: str | None = Field(
        default=None,
        env="DATABRICKS_CATALOG",
    )
    DATABRICKS_SCHEMA: str | None = Field(
        default=None,
        env="DATABRICKS_SCHEMA",
    )

    ############################################################
    # LOGGING
    ############################################################
    LOG_FILE: str = "logs/app.log"

    ############################################################
    # DATABASE URL
    ############################################################
    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:"
            f"{self.MYSQL_PASSWORD}@"
            f"{self.MYSQL_HOST}:"
            f"{self.MYSQL_PORT}/"
            f"{self.MYSQL_DB}"
        )

    @computed_field
    @property
    def SNOWFLAKE_URL(self) -> str:
        if not self.SNOWFLAKE_ACCOUNT:
            return ""

        return (
            f"snowflake://{self.SNOWFLAKE_USER}:"
            f"{self.SNOWFLAKE_PASSWORD}@"
            f"{self.SNOWFLAKE_ACCOUNT}/"
            f"{self.SNOWFLAKE_DATABASE}/"
            f"{self.SNOWFLAKE_SCHEMA}"
            f"?warehouse={self.SNOWFLAKE_WAREHOUSE}"
        )

    @computed_field
    @property
    def DATABRICKS_URL(self) -> str:
        if not self.DATABRICKS_SERVER_HOSTNAME:
            return ""

        return (
            f"databricks://token:{self.DATABRICKS_ACCESS_TOKEN}@"
            f"{self.DATABRICKS_SERVER_HOSTNAME}"
        )


@lru_cache()
def get_settings():
    return Settings()

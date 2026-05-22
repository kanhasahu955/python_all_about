from functools import lru_cache

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    ############################################################
    # APP
    ############################################################
    APP_NAME: str = "Resume AI"
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
    # PINECONE
    ############################################################
    PINECONE_API_KEY: str = Field(..., env="PINECONE_API_KEY")
    PINECONE_ENV: str = Field(..., env="PINECONE_ENV")
    PINECONE_INDEX_NAME: str = "resume-ai-index"

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


@lru_cache()
def get_settings():
    return Settings()

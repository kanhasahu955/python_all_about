from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "resume-analyzer"
    debug: bool = False

    database_url: str = "mysql+aiomysql://user:pass@127.0.0.1:3306/resume_analyzer"

    openai_api_key: str = ""

    pinecone_api_key: str = ""
    pinecone_index_name: str = "resume-analyzer"

    embedding_model: str = "text-embedding-3-small"


settings = Settings()

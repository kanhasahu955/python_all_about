from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
ENV_FILE: Path = PROJECT_ROOT / ".env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    APP_ENV: Literal["development", "staging", "production"] = Field(
        default="development",
        description="Runtime environment name.",
    )
    APP_DEBUG: bool = Field(
        default=True,
        description="Verbose/debug logging flag. Prefixed to avoid collisions "
        "with shell-level DEBUG vars (e.g. Xcode, CocoaPods).",
    )

    OPENAI_API_KEY: SecretStr | None = None
    GOOGLE_API_KEY: SecretStr | None = None
    ANTHROPIC_API_KEY: SecretStr | None = None
    GROQ_API_KEY: SecretStr | None = None
    HUGGINGFACE_API_KEY: SecretStr | None = None
    COHERE_API_KEY: SecretStr | None = None
    DEEPSEEK_API_KEY: SecretStr | None = None

    SERPER_API_KEY: SecretStr | None = Field(
        default=None,
        description="Serper.dev key for Google search tools (e.g. GoogleSerperResults).",
    )
    TAVILY_API_KEY: SecretStr | None = Field(
        default=None,
        description="Tavily API key for web search tools.",
    )

    LANGSMITH_API_KEY: SecretStr | None = None
    LANGSMITH_TRACING: bool = Field(default=False)
    LANGSMITH_PROJECT: str = Field(default="default")
    LANGSMITH_ENDPOINT: str = Field(default="https://api.smith.langchain.com")

    def export_to_os_environ(self) -> None:
        """Export configured secrets into `os.environ`.

        Several third-party SDKs (LangChain, OpenAI, etc.) read keys directly
        from `os.environ`. Call this once at app start so those libraries
        pick the values up automatically.
        """
        secret_fields = {
            "OPENAI_API_KEY": self.OPENAI_API_KEY,
            "GOOGLE_API_KEY": self.GOOGLE_API_KEY,
            "ANTHROPIC_API_KEY": self.ANTHROPIC_API_KEY,
            "GROQ_API_KEY": self.GROQ_API_KEY,
            "HUGGINGFACE_API_KEY": self.HUGGINGFACE_API_KEY,
            "COHERE_API_KEY": self.COHERE_API_KEY,
            "DEEPSEEK_API_KEY": self.DEEPSEEK_API_KEY,
            "SERPER_API_KEY": self.SERPER_API_KEY,
            "TAVILY_API_KEY": self.TAVILY_API_KEY,
            "LANGSMITH_API_KEY": self.LANGSMITH_API_KEY,
        }
        for key, value in secret_fields.items():
            if value is not None:
                os.environ[key] = value.get_secret_value()

        os.environ["LANGSMITH_TRACING"] = "true" if self.LANGSMITH_TRACING else "false"
        os.environ["LANGSMITH_PROJECT"] = self.LANGSMITH_PROJECT
        os.environ["LANGSMITH_ENDPOINT"] = self.LANGSMITH_ENDPOINT


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached `Settings` instance (singleton)."""
    return Settings()

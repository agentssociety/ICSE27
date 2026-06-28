from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Database
    database_url: str = "postgresql://app:password@localhost:5432/appdb"
    db_echo: bool = False

    # App
    app_title: str = "Generated API"
    app_version: str = "0.1.0"
    host: str = "0.0.0.0"
    port: int = 8765
    debug: bool = False

    # CORS — list of allowed origins; use ["*"] for development
    cors_origins: list[str] = ["*"]

    # Security
    secret_key: str = "change-me-in-production"


settings = Settings()

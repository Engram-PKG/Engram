from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "development"

    database_url: str = "postgresql+psycopg://digitaltwin:changeme@localhost:5432/digitaltwin"
    redis_url: str = "redis://localhost:6379/0"

    secret_key: str = "changeme-generate-a-real-secret"
    access_token_expire_minutes: int = 60 * 24

    backend_cors_origins: list[str] = ["http://localhost:8080"]

    anthropic_api_key: str | None = None

    google_client_id: str | None = None
    google_client_secret: str | None = None
    microsoft_client_id: str | None = None
    microsoft_client_secret: str | None = None
    slack_client_id: str | None = None
    slack_client_secret: str | None = None
    notion_client_id: str | None = None
    notion_client_secret: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()

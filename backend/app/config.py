from __future__ import annotations

from pydantic_settings import BaseSettings

_settings: Settings | None = None


class Settings(BaseSettings):
    postgres_url: str = "postgresql+asyncpg://app:app@postgres:5432/app"
    mongo_url: str = "mongodb://mongo:27017"
    mongo_db: str = "app"

    @property
    def postgres_dsn(self) -> str:
        return self.postgres_url.replace("+asyncpg", "", 1)

    class Config:
        env_prefix = "APP_"
        env_file = ".env"


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings

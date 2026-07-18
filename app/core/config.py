from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    APP_NAME: str
    APP_VERSION: str

    DEBUG: bool

    HOST: str
    PORT: int

    DATABASE_URL: str

    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = ""

    OWNER_EMAIL: str

    RATE_LIMIT: str = "5/minute"

    GOOGLE_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-3.5-flash"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

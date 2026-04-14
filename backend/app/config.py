from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    redis_url: str = "redis://localhost:6379/0"
    rate_limit_login_attempts: int = 5
    rate_limit_window_seconds: int = 60
    cache_ttl_seconds: int = 300
    cors_origins: str = "http://localhost:5173"

    @field_validator("access_token_expire_minutes")
    @classmethod
    def validate_expiry(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be > 0")
        return value

    @property
    def parsed_cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

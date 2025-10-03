# app/core/config.py
from typing import Any
from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # --- model configuration: load .env and ignore unknown env vars ---
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",   # ignore env vars not defined on the model
    }

    # App
    APP_NAME: str = "taskmgr"
    DEBUG: bool = False

    # Database
    DATABASE_URL: AnyUrl = Field(..., env="DATABASE_URL")

    # Security / JWT
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # default 1 day

    # Other
    S3_BUCKET: str | None = None
    S3_REGION: str | None = None


# singleton settings instance imported by other modules
settings = Settings()

from functools import lru_cache
from datetime import timedelta
from pydantic import BaseModel
from typing import Optional
import os

# PUBLIC_INTERFACE
class Settings(BaseModel):
    """Application configuration loaded from environment variables with safe defaults."""
    APP_NAME: str = "Recipe Hub API"
    APP_DESCRIPTION: str = "API for user authentication and recipe management."
    APP_VERSION: str = "0.1.0"

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "CHANGE_ME_DEV_SECRET")
    JWT_ALG: str = os.getenv("JWT_ALG", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    # CORS
    REACT_APP_BACKEND_URL: Optional[str] = os.getenv("REACT_APP_BACKEND_URL")
    REACT_APP_FRONTEND_URL: Optional[str] = os.getenv("REACT_APP_FRONTEND_URL")


@lru_cache()
# PUBLIC_INTERFACE
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()


# PUBLIC_INTERFACE
def get_access_token_expires_delta() -> timedelta:
    """Helper to convert configured minutes to timedelta for JWT expiry."""
    return timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES)

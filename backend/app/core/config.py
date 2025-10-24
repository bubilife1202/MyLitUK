"""
Configuration settings using Pydantic
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """

    # App
    APP_NAME: str = "MyLitUK"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/mylituk"

    # Redis (optional)
    REDIS_URL: Optional[str] = None

    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # External APIs
    OPEN_LIBRARY_API_URL: str = "https://openlibrary.org"
    GOOGLE_BOOKS_API_URL: str = "https://www.googleapis.com/books/v1"
    GOOGLE_BOOKS_API_KEY: Optional[str] = None

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

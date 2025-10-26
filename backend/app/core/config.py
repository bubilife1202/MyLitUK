from pydantic_settings import BaseSettings
from typing import List, Union
from pydantic import field_validator

class Settings(BaseSettings):
    # App
    APP_NAME: str = "MyLitUK"
    VERSION: str = "4.1.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./mylituk.db"

    # Redis (optional for MVP)
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # CORS - can be comma-separated string or list
    ALLOWED_ORIGINS: Union[str, List[str]] = "http://localhost:3000,http://localhost:3001,https://mylituk.vercel.app"

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    @field_validator('ALLOWED_ORIGINS', mode='before')
    @classmethod
    def parse_cors(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v

    class Config:
        env_file = ".env"

settings = Settings()

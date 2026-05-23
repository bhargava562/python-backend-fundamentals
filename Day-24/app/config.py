"""Configuration management using Pydantic Settings"""
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class AppSettings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Environment and project metadata
    ENV: Literal["development", "staging", "production"] = "development"
    PROJECT_NAME: str = "Zenovox Core API"
    VERSION: str = "1.0.0"
    
    # Core Infrastructure URLs
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres_user:password@localhost:5432/zenovox_db",
        examples=["postgresql+asyncpg://user:pass@localhost:5432/db"]
    )
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        examples=["redis://localhost:6379/0"]
    )
    CELERY_BROKER_URL: str = Field(
        default="redis://localhost:6379/0",
        examples=["redis://localhost:6379/0"]
    )
    CELERY_RESULT_BACKEND: str = Field(
        default="redis://localhost:6379/0",
        examples=["redis://localhost:6379/0"]
    )
    
    # Security parameters
    SECRET_KEY: str = Field(
        default="dev-secret-key-change-in-production",
        min_length=32
    )
    ALLOWED_HOSTS: str = "*"
    RATE_LIMIT_RULE: str = "60 per minute"
    
    # Database connection pooling
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


# Global settings instance
settings = AppSettings()

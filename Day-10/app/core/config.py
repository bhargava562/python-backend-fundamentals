from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application Configuration"""
    
    # App Settings
    app_name: str = "Day 10: Debugging & API Testing"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Server Settings
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    
    # Database Settings
    database_url: str = "sqlite:///./test.db"
    database_echo: bool = True
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Environment
    environment: str = "development"  # development, staging, production
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()

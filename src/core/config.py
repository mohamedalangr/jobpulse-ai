"""
Core configuration using Pydantic Settings.
"""
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "JobPulse AI"
    app_version: str = "0.1.0"
    environment: str = Field(default="development", alias="APP_ENV")
    database_url: str
    log_level: str = "INFO"
    debug: bool = True

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True
    )

settings = Settings()

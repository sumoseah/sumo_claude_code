"""Application configuration management."""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database Configuration
    DATABASE_URL: str = "sqlite:///./taskflow.db"

    # API Configuration
    API_V1_PREFIX: str = "/api"
    PROJECT_NAME: str = "TaskFlow API"
    PROJECT_VERSION: str = "1.0.0"

    # CORS Configuration
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173,http://localhost:8080"

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    # Logging
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @property
    def allowed_origins_list(self) -> List[str]:
        """Parse ALLOWED_ORIGINS into a list."""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


# Global settings instance
settings = Settings()

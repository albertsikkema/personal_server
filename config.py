from pydantic_settings import BaseSettings, SettingsConfigDict

from pydantic import Field, model_validator


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        validate_default=True,
    )

    # API Key for authentication
    API_KEY: str = Field(
        ...,
        min_length=8,
        description="API key for authentication (minimum 8 characters)",
    )

    # Application configuration
    APP_NAME: str = Field(default="FastAPI Application", description="Application name")
    DEBUG: bool = Field(default=True, description="Debug mode")
    ENV: str = Field(
        default="development",
        pattern="^(development|staging|production)$",
        description="Environment (development, staging, production)",
    )
    LOG_LEVEL: str = Field(
        default="INFO",
        pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$",
        description="Logging level",
    )

    # Logging configuration
    LOG_TO_FILE: bool = Field(default=True, description="Enable file logging")
    LOG_FILE_PATH: str = Field(
        default="logs", description="Directory path for log files"
    )
    LOG_FILE_NAME: str = Field(default="fastapi.log", description="Log file name")
    LOG_MAX_BYTES: int = Field(
        default=10_485_760, description="Maximum log file size in bytes (10MB)"
    )
    LOG_BACKUP_COUNT: int = Field(
        default=5, description="Number of backup log files to keep"
    )
    LOG_JSON_FORMAT: bool = Field(
        default=True,
        description="Use JSON format for file logs",
    )

    # Geocoding configuration
    GEOCODING_CACHE_TTL_HOURS: int = Field(
        default=24, description="Cache TTL for geocoding results in hours"
    )
    GEOCODING_USER_RATE_LIMIT: str = Field(
        default="10/minute",
        description="Rate limit for users calling geocoding endpoint",
    )

    @model_validator(mode="after")
    def validate_api_key(self):
        """Validate API key requirements."""
        if not self.API_KEY or len(self.API_KEY.strip()) == 0:
            raise ValueError(
                "API_KEY environment variable is required and cannot be empty"
            )
        if len(self.API_KEY) < 8:
            raise ValueError("API_KEY must be at least 8 characters long for security")
        return self


# Create a single instance to be used throughout the application
settings = Settings()

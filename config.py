from pydantic_settings import BaseSettings, SettingsConfigDict

from pydantic import Field, model_validator


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        validate_default=True,
    )

    # Legacy API Key for backward compatibility (optional now)
    API_KEY: str | None = Field(
        default=None,
        description="Legacy API key for backward compatibility",
    )

    # JWT Configuration
    JWT_SECRET: str = Field(
        ..., min_length=32, description="JWT secret key (minimum 32 characters)"
    )
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    JWT_EXPIRE_MINUTES: int = Field(default=60, description="JWT expiration in minutes")
    JWT_ISSUER: str = Field(default="fastapi-app", description="JWT issuer")
    JWT_AUDIENCE: str = Field(default="fastapi-users", description="JWT audience")

    # Database configuration
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./fastapi_users.db", description="Database URL"
    )

    # For MCP (RSA keys for production)
    JWT_PUBLIC_KEY: str | None = Field(
        default=None, description="JWT public key for MCP"
    )
    JWT_PRIVATE_KEY: str | None = Field(
        default=None, description="JWT private key for MCP"
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

    # Crawling configuration
    CRAWL4AI_BASE_URL: str = Field(
        default="https://crawl4ai.test001.nl",
        description="Base URL for Crawl4AI instance",
    )
    CRAWL4AI_API_TOKEN: str | None = Field(
        default=None,
        description="Optional JWT token for Crawl4AI authentication (if enabled on instance)",
    )
    CRAWLING_CACHE_TTL_HOURS: int = Field(
        default=1, description="Cache TTL for crawling results in hours"
    )
    CRAWLING_USER_RATE_LIMIT: str = Field(
        default="5/minute",
        description="Rate limit for users calling crawling endpoints",
    )

    @model_validator(mode="after")
    def validate_secrets(self):
        """Validate secret requirements."""
        if not self.JWT_SECRET or len(self.JWT_SECRET.strip()) == 0:
            raise ValueError(
                "JWT_SECRET environment variable is required and cannot be empty"
            )
        if len(self.JWT_SECRET) < 32:
            raise ValueError(
                "JWT_SECRET must be at least 32 characters long for security"
            )
        return self


# Create a single instance to be used throughout the application
settings = Settings()

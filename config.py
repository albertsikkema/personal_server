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

    # RSA keys (legacy fields - now used as fallback for MCP)
    JWT_PUBLIC_KEY: str | None = Field(
        default=None, description="JWT public key (legacy - fallback for MCP)"
    )
    JWT_PRIVATE_KEY: str | None = Field(
        default=None, description="JWT private key (legacy - fallback for MCP)"
    )

    # MCP-specific JWT Configuration (extends existing JWT settings)
    MCP_JWT_PRIVATE_KEY: str | None = Field(
        default=None,
        description="RSA private key for MCP JWT signing (PEM format) - fallback to JWT_PRIVATE_KEY",
    )
    MCP_JWT_PUBLIC_KEY: str | None = Field(
        default=None,
        description="RSA public key for MCP JWT verification (PEM format) - fallback to JWT_PUBLIC_KEY",
    )
    MCP_JWT_ALGORITHM: str = Field(
        default="RS256", description="RSA algorithm for MCP JWT tokens"
    )
    MCP_JWT_EXPIRE_MINUTES: int = Field(
        default=60,
        description="MCP JWT token expiration in minutes (inherits from JWT_EXPIRE_MINUTES)",
    )
    MCP_JWT_ISSUER: str = Field(
        default="personal-server", description="JWT token issuer for MCP"
    )
    MCP_JWT_AUDIENCE: str = Field(
        default="mcp-server", description="JWT token audience for MCP"
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

    # CORS configuration
    CORS_ALLOWED_ORIGINS: str = Field(
        default="*",
        description="Comma-separated list of allowed CORS origins. Use '*' for development, specific origins for production",
    )

    @model_validator(mode="after")
    def validate_secrets(self):
        """Validate secret requirements and configure MCP JWT settings."""
        # Validate main JWT secret
        if not self.JWT_SECRET or len(self.JWT_SECRET.strip()) == 0:
            raise ValueError(
                "JWT_SECRET environment variable is required and cannot be empty"
            )
        if len(self.JWT_SECRET) < 32:
            raise ValueError(
                "JWT_SECRET must be at least 32 characters long for security"
            )

        # Use fallback keys if MCP-specific keys not provided
        if not self.MCP_JWT_PRIVATE_KEY and self.JWT_PRIVATE_KEY:
            self.MCP_JWT_PRIVATE_KEY = self.JWT_PRIVATE_KEY

        if not self.MCP_JWT_PUBLIC_KEY and self.JWT_PUBLIC_KEY:
            self.MCP_JWT_PUBLIC_KEY = self.JWT_PUBLIC_KEY

        # Inherit expiration from main JWT settings if not specified
        if self.MCP_JWT_EXPIRE_MINUTES == 60 and self.JWT_EXPIRE_MINUTES != 60:
            self.MCP_JWT_EXPIRE_MINUTES = self.JWT_EXPIRE_MINUTES

        # In production, validate RSA keys
        if self.ENV == "production":
            import logging

            logger = logging.getLogger(__name__)

            if not self.MCP_JWT_PRIVATE_KEY or not self.MCP_JWT_PUBLIC_KEY:
                logger.warning(
                    "MCP will auto-generate RSA keys. "
                    "Set MCP_JWT_PRIVATE_KEY and MCP_JWT_PUBLIC_KEY for production."
                )
            else:
                # Validate PEM format for provided keys
                if not (
                    self.MCP_JWT_PRIVATE_KEY.startswith("-----BEGIN")
                    and self.MCP_JWT_PUBLIC_KEY.startswith("-----BEGIN")
                ):
                    raise ValueError(
                        "Invalid PEM format for MCP RSA keys. "
                        "Keys must be in PEM format starting with '-----BEGIN'"
                    )

        return self


# Create a single instance to be used throughout the application
settings = Settings()

import uuid
from datetime import datetime, timezone
from typing import Annotated, Optional

from config import settings
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from utils.logging import get_logger

# Get logger instance
logger = get_logger(__name__)

# Define the API key header name
api_key_header = APIKeyHeader(
    name="X-API-KEY",
    auto_error=False,  # Set to False to handle errors manually
    description="API key for authentication",
)


class AuthHTTPException(HTTPException):
    """Custom HTTPException that returns the original middleware format."""

    def __init__(self, status_code: int, message: str):
        # Create response content matching original middleware format
        self.response_content = {
            "detail": message,
            "request_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        # Pass the content as detail so FastAPI returns it directly
        super().__init__(status_code=status_code, detail=self.response_content)


async def verify_api_key(
    api_key: Annotated[Optional[str], Security(api_key_header)],
) -> str:
    """
    Verify the API key from the X-API-KEY header.

    This is the main authentication dependency for protected routes.

    Args:
        api_key: The API key from the request header

    Returns:
        The validated API key

    Raises:
        HTTPException: If the API key is missing or invalid
    """

    print(f"API Key: {api_key}")  # Debugging line to check API key
    if not api_key:
        logger.warning("API key missing in request")
        raise AuthHTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, message="API key missing"
        )

    if api_key != settings.API_KEY:
        logger.warning(
            "Invalid API key provided", extra={"provided_key_length": len(api_key)}
        )
        raise AuthHTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, message="Invalid API key"
        )

    logger.info("API key validated successfully")
    return api_key


async def optional_api_key(
    api_key: Annotated[Optional[str], Security(api_key_header)],
) -> Optional[str]:
    """
    Optional API key verification for routes that can work with or without authentication.

    This dependency allows endpoints to be accessed without authentication but provides
    the API key if present and valid.

    Args:
        api_key: The API key from the request header (optional)

    Returns:
        The validated API key if provided and valid, None otherwise

    Raises:
        HTTPException: Only if an API key is provided but invalid
    """
    if not api_key:
        return None

    if api_key != settings.API_KEY:
        logger.warning(
            "Invalid API key provided in optional auth",
            extra={"provided_key_length": len(api_key)},
        )
        raise AuthHTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, message="Invalid API key"
        )

    logger.info("Optional API key validated successfully")
    return api_key


# Helper dependency aliases for easier use in routes
RequiredAuth = Depends(verify_api_key)
OptionalAuth = Depends(optional_api_key)

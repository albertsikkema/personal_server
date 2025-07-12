import uuid
from datetime import UTC, datetime

from fastapi.responses import JSONResponse
from utils.logging import get_logger

# Get logger instance
logger = get_logger(__name__)


# Standardized error response format for API errors, currently not used in the codebase
def create_error_response(
    status_code: int, detail: str, request_id: str | None = None
) -> JSONResponse:
    """
    Create standardized error response with request ID and timestamp.

    Args:
        status_code: HTTP status code
        detail: Error detail message
        request_id: Optional request ID (generated if not provided)

    Returns:
        JSONResponse with standardized error format
    """
    if request_id is None:
        request_id = str(uuid.uuid4())

    return JSONResponse(
        status_code=status_code,
        content={
            "detail": detail,
            "request_id": request_id,
            "timestamp": datetime.now(UTC).isoformat(),
        },
    )

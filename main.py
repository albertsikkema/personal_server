from datetime import datetime, timezone

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from config import settings
from dependencies import AuthHTTPException, RequiredAuth
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routers import crawling, geocoding
from utils.logging import get_logger, setup_logging

# Initialize logging configuration
setup_logging()
logger = get_logger(__name__)

# Create FastAPI instance
app = FastAPI(
    title="FastAPI Application",
    description="A FastAPI application with API key authentication",
    version="1.0.0",
    # Hide docs in production environment
    docs_url="/docs" if settings.ENV != "production" else None,
    redoc_url="/redoc" if settings.ENV != "production" else None,
    openapi_url="/openapi.json" if settings.ENV != "production" else None,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize global rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include routers
app.include_router(
    geocoding.router,
    responses={
        401: {"description": "Authentication required"},
        404: {"description": "City not found"},
        429: {"description": "Rate limit exceeded"},
        503: {"description": "Service unavailable"},
    },
)

app.include_router(
    crawling.router,
    responses={
        401: {"description": "Authentication required"},
        422: {"description": "Invalid input parameters"},
        429: {"description": "Rate limit exceeded"},
        503: {"description": "Crawl4AI service unavailable"},
    },
)


# Add custom exception handler for authentication errors
@app.exception_handler(AuthHTTPException)
async def auth_exception_handler(_request: Request, exc: AuthHTTPException):
    """Handle authentication exceptions with the original middleware format."""
    return JSONResponse(status_code=exc.status_code, content=exc.response_content)


# Root endpoint (no authentication required)
@app.get("/")
async def root():
    """
    Root endpoint without authentication.

    Returns:
        A welcome message
    """
    return {"message": "Welcome to FastAPI Application"}


# Health check endpoint (no authentication required)
@app.get("/health")
async def health_check():
    """
    Health check endpoint without authentication.

    Returns:
        A dictionary with health status information
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "FastAPI Application",
        "version": "1.0.0",
    }


# Protected endpoint (authentication required via dependency)
@app.get("/protected")
async def protected_endpoint(_api_key: str = RequiredAuth):
    """
    Protected endpoint that requires API key authentication.
    Authentication is handled by dependency injection.

    Args:
        api_key: The validated API key from the dependency

    Returns:
        A message confirming access to protected resource
    """
    return {
        "message": "Access granted to protected resource",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# Another protected endpoint example
@app.get("/protected/data")
async def protected_data(_api_key: str = RequiredAuth):
    """
    Another protected endpoint example.

    Args:
        api_key: The validated API key from the dependency

    Returns:
        Some protected data
    """
    return {
        "data": {
            "id": 1,
            "info": "This is protected information",
            "items": ["item1", "item2", "item3"],
        }
    }

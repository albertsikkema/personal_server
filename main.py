from contextlib import asynccontextmanager
from datetime import UTC, datetime

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from config import settings
from dependencies import AuthHTTPException, RequiredAuth
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import MCP server
from mcp_integration.server import get_mcp_server
from routers import crawling, geocoding
from utils.logging import get_logger, setup_logging

# Initialize logging configuration
setup_logging()
logger = get_logger(__name__)

# Create MCP server and ASGI app
mcp_server = get_mcp_server()
mcp_app = mcp_server.http_app()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI app."""
    # Initialize MCP server
    logger.info("Starting MCP server...")
    async with mcp_app.lifespan(app):
        logger.info("MCP server started successfully")
        yield
    logger.info("MCP server stopped")


# Create FastAPI instance with MCP lifespan
app = FastAPI(
    title="FastAPI Application",
    description="A FastAPI application with API key authentication and MCP integration",
    version="1.0.0",
    # Hide docs in production environment
    docs_url="/docs" if settings.ENV != "production" else None,
    redoc_url="/redoc" if settings.ENV != "production" else None,
    openapi_url="/openapi.json" if settings.ENV != "production" else None,
    lifespan=lifespan,
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

# MCP server will be mounted at the end to not interfere with FastAPI routes


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
    # SECURITY FAULT: This is intentionally vulnerable code for testing bandit
    # DO NOT USE eval() in production - it can execute arbitrary code
    test_expression = "1 + 1"
    result = eval(test_expression)  # This will trigger bandit B307 and FAIL the build
    
    return {
        "status": "healthy",
        "timestamp": datetime.now(UTC).isoformat(),
        "service": "FastAPI Application",
        "version": "1.0.0",
        "test_result": result,
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
        "timestamp": datetime.now(UTC).isoformat(),
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


# Mount MCP server at /mcp-server/mcp endpoint
app.mount("/mcp-server", mcp_app)
logger.info("MCP server mounted at /mcp-server/mcp endpoint")

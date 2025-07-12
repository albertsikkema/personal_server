from contextlib import asynccontextmanager
from datetime import UTC, datetime

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from auth.backend import auth_backend

# Authentication imports
from auth.users import current_active_user, fastapi_users
from config import settings

# Database imports
from database import close_db, create_db_and_tables
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import MCP server
from mcp_integration.server import get_mcp_server
from routers import crawling, geocoding, mcp_auth
from schemas.user import UserCreate, UserRead, UserUpdate
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
    # Initialize database
    logger.info("Creating database tables...")
    await create_db_and_tables()
    logger.info("Database tables created successfully")

    # Initialize MCP server
    logger.info("Starting MCP server...")
    async with mcp_app.lifespan(app):
        logger.info("MCP server started successfully")
        yield

    # Cleanup
    logger.info("Closing database connections...")
    await close_db()
    logger.info("MCP server and database stopped")


# Create FastAPI instance with database and MCP lifespan
app = FastAPI(
    title="FastAPI Application with JWT Authentication",
    description="A FastAPI application with JWT Bearer token authentication, user management, and MCP integration",
    version="1.0.0",
    # Hide docs in production environment
    docs_url="/docs" if settings.ENV != "production" else None,
    redoc_url="/redoc" if settings.ENV != "production" else None,
    openapi_url="/openapi.json" if settings.ENV != "production" else None,
    lifespan=lifespan,
)

# Configure CORS based on environment
cors_origins = (
    settings.CORS_ALLOWED_ORIGINS.split(",")
    if settings.CORS_ALLOWED_ORIGINS != "*"
    else ["*"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Initialize global rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include authentication routes
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
    responses={
        400: {"description": "Bad Request"},
        401: {"description": "Invalid credentials"},
        422: {"description": "Validation Error"},
    },
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
    responses={
        400: {"description": "Bad Request"},
        422: {"description": "Validation Error"},
    },
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Not enough permissions"},
        404: {"description": "User not found"},
        422: {"description": "Validation Error"},
    },
)

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

# Include MCP authentication router
app.include_router(
    mcp_auth.router,
    responses={
        401: {"description": "Authentication required"},
        500: {"description": "Token generation failed"},
    },
)

# MCP server will be mounted at the end to not interfere with FastAPI routes


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
        "timestamp": datetime.now(UTC).isoformat(),
        "service": "FastAPI Application",
        "version": "1.0.0",
    }


# Protected endpoint (authentication required via JWT Bearer token)
@app.get("/protected")
async def protected_endpoint(user=Depends(current_active_user)):
    """
    Protected endpoint that requires JWT Bearer token authentication.
    Authentication is handled by FastAPI-Users dependency injection.

    Args:
        user: The authenticated user from the JWT token

    Returns:
        A message confirming access to protected resource with user info
    """
    return {
        "message": "Access granted to protected resource",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
        },
        "timestamp": datetime.now(UTC).isoformat(),
    }


# Another protected endpoint example
@app.get("/protected/data")
async def protected_data(user=Depends(current_active_user)):
    """
    Another protected endpoint example using JWT Bearer token authentication.

    Args:
        user: The authenticated user from the JWT token

    Returns:
        Some protected data
    """
    return {
        "data": {
            "id": 1,
            "info": "This is protected information",
            "items": ["item1", "item2", "item3"],
            "accessible_by": user.email,
        }
    }


# Mount MCP server at /mcp-server/mcp endpoint
app.mount("/mcp-server", mcp_app)
logger.info("MCP server mounted at /mcp-server/mcp endpoint")

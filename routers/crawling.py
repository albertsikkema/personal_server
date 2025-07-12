"""
FastAPI router for crawling endpoints.

This module provides RESTful endpoints for web crawling functionality,
including screenshot capture, link extraction, and caching.
"""

from datetime import datetime

import httpx
from slowapi import Limiter
from slowapi.util import get_remote_address

from auth.users import current_active_user
from config import settings
from fastapi import APIRouter, Depends, HTTPException, Request
from models.crawling import (
    CacheClearResponse,
    CrawlRequest,
    CrawlingHealthResponse,
    CrawlingResponse,
)
from models.user import User
from pydantic import ValidationError
from services.crawling import get_crawling_service

# Rate limiter for user requests
limiter = Limiter(key_func=get_remote_address)

# Router configuration
router = APIRouter(
    prefix="/crawl",
    tags=["crawling"],
    # Authentication is now handled per-endpoint for better user tracking
    responses={
        401: {"description": "Authentication required (JWT Bearer token)"},
        429: {"description": "Rate limit exceeded"},
        503: {"description": "Service temporarily unavailable"},
    },
)


@router.post(
    "",
    response_model=CrawlingResponse,
    summary="Crawl URLs",
    description="""
    Crawl one or more URLs and extract content.
    
    Features:
    - Multi-URL support (1-10 URLs per request)
    - Markdown extraction with optional HTML and metadata
    - Internal and external link extraction
    - Screenshot capture with custom dimensions (320x240 to 3840x2160)
    - Intelligent caching with TTL
    - Rate limiting for API protection
    
    Screenshot dimensions are validated to prevent abuse:
    - Width: 320-3840 pixels (mobile to 4K width)
    - Height: 240-2160 pixels (mobile to 4K height)
    - Aspect ratio: 0.5:1 to 4:1 (prevents extremely wide/tall images)
    
    Cache modes:
    - enabled: Use cache if available, store new results
    - disabled: Don't use or store cache
    - bypass: Ignore existing cache but store new results
    """,
    responses={
        200: {
            "description": "Crawling completed",
            "content": {
                "application/json": {
                    "example": {
                        "total_urls": 2,
                        "successful_crawls": 2,
                        "failed_crawls": 0,
                        "cached_results": 0,
                        "results": [
                            {
                                "url": "https://example.com",
                                "success": True,
                                "markdown": "# Example Domain\\n\\nThis domain is for use in illustrative examples...",
                                "cleaned_html": "<h1>Example Domain</h1><p>This domain is for use...</p>",
                                "metadata": {
                                    "title": "Example Domain",
                                    "description": "Example domain description",
                                },
                                "internal_links": ["https://example.com/about"],
                                "external_links": ["https://www.iana.org/domains"],
                                "screenshot_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
                                "screenshot_size": {"width": 1920, "height": 1080},
                                "status_code": 200,
                                "crawl_time_seconds": 2.5,
                            }
                        ],
                        "timestamp": "2024-01-01T12:00:00",
                        "total_time_seconds": 3.2,
                    }
                }
            },
        },
        422: {"description": "Invalid input parameters"},
        503: {"description": "Crawl4AI service unavailable"},
    },
)
@limiter.limit(settings.CRAWLING_USER_RATE_LIMIT)
async def crawl_urls(
    request: Request,  # Required for rate limiter  # noqa: ARG001
    crawl_request: CrawlRequest,
    user: User = Depends(  # noqa: ARG001 - Required for auth but not used in logic
        current_active_user
    ),  # JWT Bearer token authentication
) -> CrawlingResponse:
    """
    Crawl URLs and extract content with optional screenshots and link extraction.

    Args:
        request: FastAPI request object (required for rate limiting)
        crawl_request: Crawling configuration and URL list
        _api_key: API key for authentication (injected by dependency)

    Returns:
        CrawlingResponse with results for all requested URLs

    Raises:
        HTTPException: For service errors or invalid requests
    """
    try:
        service = get_crawling_service()
        result = await service.crawl_urls(crawl_request)
        return result

    except httpx.ConnectError as e:
        # Log the error for debugging
        import logging

        logger = logging.getLogger(__name__)
        logger.error(f"Crawl4AI service unreachable: {e!s}")

        raise HTTPException(
            status_code=503, detail="Crawl4AI service unreachable"
        ) from e
    except httpx.TimeoutException as e:
        # Log the error for debugging
        import logging

        logger = logging.getLogger(__name__)
        logger.error(f"Crawl4AI service timeout: {e!s}")

        raise HTTPException(status_code=504, detail="Crawl4AI service timeout") from e
    except ValidationError as e:
        # Log the error for debugging
        import logging

        logger = logging.getLogger(__name__)
        logger.error(f"Invalid crawl configuration: {e!s}")

        raise HTTPException(
            status_code=422, detail=f"Invalid crawl configuration: {e!s}"
        ) from e
    except Exception as e:
        # Log the error for debugging
        import logging

        logger = logging.getLogger(__name__)
        logger.error(f"Crawling failed: {e!s}")

        raise HTTPException(
            status_code=503,
            detail=f"Crawling service temporarily unavailable: {e!s}",
        ) from e


@router.get(
    "/health",
    response_model=CrawlingHealthResponse,
    summary="Crawling service health check",
    description="""
    Check the health and status of the crawling service.
    
    Returns information about:
    - Service status (healthy/degraded)
    - Cache statistics (size, TTL, expired entries)
    - Rate limiter status
    - Crawl4AI instance connectivity
    - Crawl4AI service health
    
    This endpoint is useful for monitoring and debugging crawling issues.
    """,
    responses={
        200: {
            "description": "Health check completed",
            "content": {
                "application/json": {
                    "example": {
                        "service": "crawling",
                        "status": "healthy",
                        "cache_size": 42,
                        "cache_ttl_hours": 1,
                        "rate_limiter_active": True,
                        "crawl4ai_instance": "https://crawl4ai.test001.nl",
                        "crawl4ai_healthy": True,
                        "crawl4ai_response": {
                            "status": "healthy",
                            "version": "0.6.0",
                            "uptime": "2h 30m",
                        },
                    }
                }
            },
        }
    },
)
@limiter.limit(settings.CRAWLING_USER_RATE_LIMIT)
async def health_check(
    request: Request,  # Required for rate limiter  # noqa: ARG001
    user: User = Depends(  # noqa: ARG001 - Required for auth but not used in logic
        current_active_user
    ),  # JWT Bearer token authentication
) -> CrawlingHealthResponse:
    """
    Get comprehensive health status of the crawling service.

    Args:
        request: FastAPI request object (required for rate limiting)
        _api_key: API key for authentication (injected by dependency)

    Returns:
        CrawlingHealthResponse with service status and statistics
    """
    service = get_crawling_service()
    return await service.get_health_response()


@router.post(
    "/cache/clear",
    response_model=CacheClearResponse,
    summary="Clear crawling cache",
    description="""
    Clear all cached crawling results.
    
    This endpoint removes all cached crawling data, forcing fresh crawls
    for subsequent requests. Use this when you need to ensure fresh data
    or when debugging caching issues.
    
    The response includes the number of cache entries that were cleared.
    """,
    responses={
        200: {
            "description": "Cache cleared successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Cache cleared successfully. 42 entries removed.",
                        "cleared_entries": 42,
                        "timestamp": "2024-01-01T12:00:00",
                    }
                }
            },
        }
    },
)
@limiter.limit(settings.CRAWLING_USER_RATE_LIMIT)
async def clear_cache(
    request: Request,  # Required for rate limiter  # noqa: ARG001
    user: User = Depends(  # noqa: ARG001 - Required for auth but not used in logic
        current_active_user
    ),  # JWT Bearer token authentication
) -> CacheClearResponse:
    """
    Clear all cached crawling results.

    Args:
        request: FastAPI request object (required for rate limiting)
        _api_key: API key for authentication (injected by dependency)

    Returns:
        CacheClearResponse with operation details
    """
    service = get_crawling_service()
    return service.clear_cache_response()


# Additional administrative endpoints (optional, for future use)


@router.post(
    "/cache/cleanup",
    response_model=dict,
    summary="Cleanup expired cache entries",
    description="""
    Remove only expired cache entries, keeping valid ones.
    
    This is a maintenance endpoint that removes expired cache entries
    without affecting valid cached data. It's automatically performed
    during normal operations but can be manually triggered.
    """,
    include_in_schema=False,  # Hidden from main API docs
)
@limiter.limit(settings.CRAWLING_USER_RATE_LIMIT)
async def cleanup_expired_cache(
    request: Request,  # Required for rate limiter  # noqa: ARG001
    user: User = Depends(  # noqa: ARG001 - Required for auth but not used in logic
        current_active_user
    ),  # JWT Bearer token authentication
) -> dict:
    """
    Clean up expired cache entries.

    Args:
        request: FastAPI request object
        _api_key: API key for authentication

    Returns:
        Cleanup operation details
    """
    service = get_crawling_service()
    cleaned_count = service.cleanup_expired_cache()

    return {
        "message": f"Cleanup completed. {cleaned_count} expired entries removed.",
        "cleaned_entries": cleaned_count,
        "timestamp": datetime.now().isoformat(),
    }


@router.get(
    "/cache/stats",
    response_model=dict,
    summary="Get detailed cache statistics",
    description="""
    Get detailed statistics about the crawling cache.
    
    Provides information about cache size, TTL, expired entries,
    and other cache metrics useful for monitoring and optimization.
    """,
    include_in_schema=False,  # Hidden from main API docs
)
@limiter.limit(settings.CRAWLING_USER_RATE_LIMIT)
async def get_cache_stats(
    request: Request,  # Required for rate limiter  # noqa: ARG001
    user: User = Depends(  # noqa: ARG001 - Required for auth but not used in logic
        current_active_user
    ),  # JWT Bearer token authentication
) -> dict:
    """
    Get detailed cache statistics.

    Args:
        request: FastAPI request object
        _api_key: API key for authentication

    Returns:
        Detailed cache statistics
    """
    service = get_crawling_service()
    return service.get_cache_stats()

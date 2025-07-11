"""
Geocoding API router with rate limiting and authentication.

This module defines API endpoints for geocoding functionality including:
- City name to coordinates conversion
- Health check for geocoding service
- Comprehensive error handling and validation

All endpoints require API key authentication and implement user rate limiting
in addition to the Nominatim API rate limiting handled by the service layer.
"""

from datetime import UTC, datetime

from slowapi import Limiter
from slowapi.util import get_remote_address

from config import settings
from dependencies import RequiredAuth
from fastapi import APIRouter, HTTPException, Query, Request
from models.geocoding import GeocodingResponse
from services.geocoding import GeocodingService
from utils.logging import get_logger

logger = get_logger(__name__)

# Initialize limiter for this router
limiter = Limiter(key_func=get_remote_address)

# Create router with authentication and tags
router = APIRouter(
    prefix="/geocode",
    tags=["geocoding"],
    dependencies=[RequiredAuth],  # Apply auth to all routes in this router
)

# Initialize geocoding service (singleton pattern)
geocoding_service = GeocodingService()


@router.get("/city", response_model=GeocodingResponse)
@limiter.limit(settings.GEOCODING_USER_RATE_LIMIT)
async def geocode_city(
    request: Request,  # Required for rate limiter
    city: str = Query(
        ...,
        min_length=1,
        max_length=200,
        description="City name to geocode",
        examples=["London", "New York", "Tokyo", "São Paulo"],
    ),
):
    """
    Geocode a city name to geographic coordinates.

    This endpoint uses the Nominatim geocoding service to convert
    city names into latitude and longitude coordinates. Results are
    cached to improve performance and reduce API calls.

    **Rate Limits:**
    - User limit: 10 requests per minute per IP
    - Nominatim API: 1 request per second (handled internally)

    **Caching:**
    - Results are cached for 24 hours by default
    - Cache hits are indicated in the response

    **Authentication:**
    - Requires valid API key in X-API-KEY header

    Args:
        request: FastAPI request object (required for rate limiting)
        city: The name of the city to geocode (1-200 characters)

    Returns:
        GeocodingResponse: Geographic coordinates and location details

    Raises:
        HTTPException 401: If authentication is invalid
        HTTPException 404: If city is not found
        HTTPException 422: If input validation fails
        HTTPException 429: If rate limit is exceeded
        HTTPException 503: If geocoding service is unavailable

    Example:
        ```
        GET /geocode/city?city=London

        Response:
        {
            "city": "London",
            "location": {
                "lat": 51.5074,
                "lon": -0.1278
            },
            "display_name": "London, Greater London, England, United Kingdom",
            "place_id": 12345,
            "boundingbox": [51.2868, 51.6918, -0.5103, 0.3340],
            "timestamp": "2024-01-01T12:00:00+00:00",
            "cached": false
        }
        ```
    """
    logger.info(
        f"Geocoding API request for city: '{city}' from IP: {get_remote_address(request)}"
    )

    try:
        result = await geocoding_service.geocode_city(city)

        if not result:
            logger.warning(f"City not found: '{city}'")
            raise HTTPException(status_code=404, detail=f"City '{city}' not found")

        logger.info(
            f"Geocoding API successful for city: '{city}', "
            f"cached: {result.cached}, coords: ({result.location.lat}, {result.location.lon})"
        )
        return result

    except HTTPException:
        # Re-raise HTTP exceptions as-is (like 404 from above)
        raise
    except Exception as e:
        logger.error(f"Geocoding service error for city '{city}': {e!s}")
        raise HTTPException(
            status_code=503, detail="Geocoding service temporarily unavailable"
        ) from e


@router.get("/health")
@limiter.limit("60/minute")  # Higher limit for health checks
async def geocoding_health(request: Request):
    """
    Health check endpoint for geocoding service.

    Provides status information about the geocoding service including
    cache statistics and service availability.

    Args:
        request: FastAPI request object (required for rate limiting)

    Returns:
        Service health status and cache statistics

    Example:
        ```
        GET /geocode/health

        Response:
        {
            "service": "geocoding",
            "status": "healthy",
            "cache_size": 42,
            "cache_ttl_hours": 24,
            "rate_limiter": "active",
            "user_agent": "FastAPI Application/1.0"
        }
        ```
    """
    logger.debug(f"Geocoding health check from IP: {get_remote_address(request)}")

    try:
        cache_stats = geocoding_service.get_cache_stats()

        return {"service": "geocoding", "status": "healthy", **cache_stats}

    except Exception as e:
        logger.error(f"Geocoding health check failed: {e!s}")
        raise HTTPException(
            status_code=503, detail="Geocoding service health check failed"
        ) from e


@router.post("/cache/clear")
@limiter.limit("10/hour")  # Very limited for admin operations
async def clear_geocoding_cache(request: Request):
    """
    Clear the geocoding cache.

    Administrative endpoint to clear all cached geocoding results.
    Use sparingly as this will increase API calls to Nominatim.

    Args:
        request: FastAPI request object (required for rate limiting)

    Returns:
        Cache clear confirmation

    Example:
        ```
        POST /geocode/cache/clear

        Response:
        {
            "message": "Geocoding cache cleared",
            "timestamp": "2024-01-01T12:00:00+00:00"
        }
        ```
    """
    logger.warning(f"Cache clear requested from IP: {get_remote_address(request)}")

    try:
        geocoding_service.clear_cache()

        return {
            "message": "Geocoding cache cleared",
            "timestamp": datetime.now(UTC).isoformat(),
        }

    except Exception as e:
        logger.error(f"Cache clear failed: {e!s}")
        raise HTTPException(
            status_code=503, detail="Failed to clear geocoding cache"
        ) from e

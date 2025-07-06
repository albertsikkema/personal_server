"""
Geocoding service using Nominatim HTTP API.

This module provides geocoding functionality that converts city names to
geographic coordinates. It integrates rate limiting and caching to comply
with Nominatim's usage policy and improve performance.

CRITICAL: Must comply with Nominatim usage policy:
- Maximum 1 request per second
- Must provide User-Agent header
- Must cache results to minimize API calls
"""

from datetime import datetime, timezone
from typing import Optional

import httpx

from config import settings
from models.geocoding import GeocodingResponse, Location
from services.cache import GeocodingCache
from services.rate_limiter import RateLimiter
from utils.logging import get_logger

logger = get_logger(__name__)


class GeocodingService:
    """
    Service for geocoding city names to coordinates using Nominatim HTTP API.

    Implements comprehensive rate limiting and caching to ensure compliance
    with Nominatim's usage policy while providing efficient geocoding.

    Features:
    - Rate limiting (1 req/sec max) for Nominatim compliance
    - Caching with configurable TTL to reduce API calls
    - Proper User-Agent header for API compliance
    - Comprehensive error handling and logging
    """

    def __init__(self):
        """
        Initialize the geocoding service with rate limiting and caching.
        """
        self.rate_limiter = RateLimiter(max_requests=1, time_window=1.0)
        self.cache = GeocodingCache(ttl_hours=settings.GEOCODING_CACHE_TTL_HOURS)
        self.user_agent = f"{settings.APP_NAME}/1.0"
        self.base_url = "https://nominatim.openstreetmap.org"

        logger.info(
            f"GeocodingService initialized with cache TTL: "
            f"{settings.GEOCODING_CACHE_TTL_HOURS}h, user-agent: {self.user_agent}"
        )

    async def geocode_city(self, city: str) -> Optional[GeocodingResponse]:
        """
        Geocode a city name to coordinates using Nominatim HTTP API.

        Implements caching and rate limiting to respect API limits and
        improve performance. Uses the first result from Nominatim if
        multiple results are returned.

        Args:
            city: City name to geocode

        Returns:
            GeocodingResponse with coordinates and metadata, or None if not found

        Raises:
            Exception: If Nominatim API encounters an error
        """
        logger.info(f"Geocoding request for city: '{city}'")

        # Check cache first
        cached = self.cache.get(city)
        if cached:
            logger.info(f"Cache hit for city: '{city}'")
            response = GeocodingResponse(**cached)
            response.cached = True
            return response

        # Rate limit before API call to ensure Nominatim compliance
        logger.debug(f"Cache miss for city: '{city}' - making API call")
        await self.rate_limiter.acquire()

        try:
            # Prepare request parameters
            params = {
                "q": city,
                "format": "json",
                "addressdetails": "1",
                "limit": "5",  # Get multiple results for better accuracy
                "accept-language": "en",  # Prefer English responses
            }

            headers = {"User-Agent": self.user_agent}

            logger.debug(f"Calling Nominatim HTTP API for city: '{city}'")

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/search",
                    params=params,
                    headers=headers,
                    timeout=10.0,
                )
                response.raise_for_status()

                results = response.json()

                if not results:
                    logger.info(f"No results found for city: '{city}'")
                    return None

                # Use first result (most relevant)
                result = results[0]
                logger.debug(
                    f"Nominatim returned {len(results)} results for '{city}', "
                    f"using first: {result.get('display_name', 'N/A')}"
                )

                # Extract bounding box if present
                boundingbox = None
                if result.get("boundingbox"):
                    try:
                        boundingbox = [float(x) for x in result["boundingbox"]]
                    except (ValueError, TypeError):
                        logger.warning(f"Invalid boundingbox format for city '{city}'")

                # Build response object
                geocoding_response = GeocodingResponse(
                    city=city,
                    location=Location(
                        lat=float(result["lat"]), lon=float(result["lon"])
                    ),
                    display_name=result.get("display_name", city),
                    place_id=int(result.get("place_id", 0))
                    if result.get("place_id")
                    else None,
                    boundingbox=boundingbox,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    cached=False,
                )

                # Cache the result for future requests
                self.cache.set(city, geocoding_response.model_dump())

                logger.info(
                    f"Geocoding successful for city: '{city}' -> "
                    f"({geocoding_response.location.lat}, {geocoding_response.location.lon})"
                )
                return geocoding_response

        except httpx.HTTPStatusError as e:
            logger.error(
                f"HTTP error from Nominatim API for city '{city}': {e.response.status_code}"
            )
            raise Exception(
                f"Nominatim API HTTP error: {e.response.status_code}"
            ) from e
        except httpx.TimeoutException as e:
            logger.error(f"Timeout error from Nominatim API for city '{city}'")
            raise Exception("Nominatim API timeout") from e
        except Exception as e:
            logger.error(f"Geocoding error for city '{city}': {e!s}")
            raise

    def get_cache_stats(self) -> dict:
        """
        Get cache statistics for monitoring and health checks.

        Returns:
            Dictionary with cache size and configuration info
        """
        return {
            "cache_size": self.cache.size(),
            "cache_ttl_hours": settings.GEOCODING_CACHE_TTL_HOURS,
            "rate_limiter": "active",
            "user_agent": self.user_agent,
        }

    def clear_cache(self):
        """
        Clear the geocoding cache.

        Useful for testing or cache management.
        """
        self.cache.clear()
        logger.info("Geocoding cache cleared")

    def cleanup_expired_cache(self) -> int:
        """
        Remove expired entries from cache.

        Returns:
            Number of expired entries removed
        """
        return self.cache.cleanup_expired()

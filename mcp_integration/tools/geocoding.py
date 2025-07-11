"""
Geocoding Tool for FastMCP.

This module provides the geocoding tool that reuses the existing geocoding
service to convert city names to geographic coordinates via MCP.
"""

import logging
from typing import Annotated, Optional

from fastmcp import FastMCP

# Import existing services and models
from pydantic import Field
from services.geocoding import GeocodingService

# Global service instance
_geocoding_service: Optional[GeocodingService] = None

# Create MCP instance for tool decoration
mcp = FastMCP("GecodingTools")

# Setup logging
logger = logging.getLogger(__name__)


def get_geocoding_service() -> GeocodingService:
    """
    Get or create the geocoding service instance.

    Returns:
        GeocodingService: The geocoding service instance
    """
    global _geocoding_service
    if _geocoding_service is None:
        _geocoding_service = GeocodingService()
    return _geocoding_service


async def _geocode_city_impl(city: str) -> dict:
    """
    Implementation of the geocode_city function.

    This is the actual implementation that can be called directly for testing.
    """
    try:
        # Validate city parameter
        if not city or len(city.strip()) == 0:
            return {
                "error": "Invalid input",
                "city": city,
                "message": "City name cannot be empty",
            }

        # Get geocoding service
        service = get_geocoding_service()

        # Perform geocoding
        result = await service.geocode_city(city.strip())

        if result is None:
            return {
                "error": "City not found",
                "city": city,
                "message": "No geocoding results found for the specified city",
            }

        # Convert to dict for MCP response
        response_dict = result.model_dump()
        response_dict["success"] = True

        return response_dict

    except Exception as e:
        # Import httpx here to avoid circular imports
        import httpx

        # Categorize errors for better debugging
        if isinstance(e, (httpx.ConnectError, httpx.TimeoutException)):
            logger.error(f"Network error for city '{city}': {e}")
            return {"error": "Network error", "city": city, "message": str(e)}
        else:
            logger.error(f"Unexpected error for city '{city}': {e}")
            return {"error": "Service error", "city": city, "message": str(e)}


@mcp.tool()
async def geocode_city(
    city: Annotated[
        str,
        Field(
            description="City name to geocode (1-200 characters)",
            min_length=1,
            max_length=200,
        ),
    ],
) -> dict:
    """
    Geocode a city name to get its geographic coordinates.

    This tool converts city names to geographic coordinates using OpenStreetMap's
    Nominatim service. Results include latitude, longitude, display name, and
    optional bounding box information.

    Features:
    - Caching with 24-hour TTL
    - Rate limiting (1 request/second to Nominatim)
    - Comprehensive error handling
    - Identical behavior to REST API endpoint

    Args:
        city: The name of the city to geocode

    Returns:
        dict: Geocoding result with location data or error information

    Examples:
        >>> await geocode_city("London")
        {
            "success": True,
            "city": "London",
            "location": {"lat": 51.5074, "lon": -0.1278},
            "display_name": "London, Greater London, England, United Kingdom",
            "place_id": 12345,
            "boundingbox": [51.2868, 51.6918, -0.5103, 0.3340],
            "timestamp": "2024-01-01T12:00:00+00:00",
            "cached": false
        }

        >>> await geocode_city("NonexistentCity")
        {
            "error": "City not found",
            "city": "NonexistentCity",
            "message": "No geocoding results found for the specified city"
        }
    """
    return await _geocode_city_impl(city)


def reset_geocoding_service() -> None:
    """
    Reset the geocoding service instance.

    This is primarily useful for testing purposes.
    """
    global _geocoding_service
    _geocoding_service = None

"""
Pydantic models for geocoding functionality.

This module defines the data models used for geocoding requests and responses,
including validation rules and serialization formats.
"""

from typing import Optional

from pydantic import BaseModel, Field


class GeocodingRequest(BaseModel):
    """
    Request model for geocoding operations.

    Args:
        city: City name to geocode (1-200 characters)
    """

    city: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="City name to geocode",
        examples=["London", "New York", "Tokyo"],
    )


class Location(BaseModel):
    """
    Geographic location model containing latitude and longitude coordinates.

    Args:
        lat: Latitude in decimal degrees
        lon: Longitude in decimal degrees
    """

    lat: float = Field(
        ...,
        description="Latitude in decimal degrees",
        ge=-90.0,
        le=90.0,
        examples=[51.5074, -0.1278],
    )
    lon: float = Field(
        ...,
        description="Longitude in decimal degrees",
        ge=-180.0,
        le=180.0,
        examples=[-0.1278, 13.4050],
    )


class GeocodingResponse(BaseModel):
    """
    Response model for successful geocoding operations.

    Contains the requested city name, geographic coordinates, and additional
    metadata from the geocoding service.

    Args:
        city: The original requested city name
        location: Geographic coordinates (lat, lon)
        display_name: Full formatted address from geocoding service
        place_id: Unique identifier from geocoding service (optional)
        boundingbox: Geographic bounding box [min_lat, max_lat, min_lon, max_lon] (optional)
        timestamp: ISO formatted timestamp of the response
        cached: Whether this result was retrieved from cache
    """

    city: str = Field(..., description="Requested city name", examples=["London"])
    location: Location = Field(..., description="Geographic coordinates")
    display_name: str = Field(
        ...,
        description="Full formatted address from geocoding service",
        examples=["London, Greater London, England, United Kingdom"],
    )
    place_id: Optional[int] = Field(
        None, description="Nominatim place ID", examples=[12345]
    )
    boundingbox: Optional[list[float]] = Field(
        None,
        description="Bounding box [min_lat, max_lat, min_lon, max_lon]",
        min_length=4,
        max_length=4,
        examples=[[51.2868, 51.6918, -0.5103, 0.3340]],
    )
    timestamp: str = Field(
        ...,
        description="Response timestamp in ISO format",
        examples=["2024-01-01T12:00:00+00:00"],
    )
    cached: bool = Field(
        default=False, description="Whether this result was from cache"
    )

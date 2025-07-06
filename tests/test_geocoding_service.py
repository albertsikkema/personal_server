import time
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from models.geocoding import GeocodingResponse, Location
from services.geocoding import GeocodingService


@pytest.mark.asyncio
async def test_geocode_city_success():
    """Test successful geocoding."""
    service = GeocodingService()

    # Mock HTTP response
    mock_response_data = [
        {
            "lat": "52.520008",
            "lon": "13.404954",
            "display_name": "Berlin, Germany",
            "place_id": "12345",
            "boundingbox": ["52.3", "52.7", "13.1", "13.7"],
        }
    ]

    with patch("httpx.AsyncClient") as mock_client:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status.return_value = None

        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        result = await service.geocode_city("Berlin")

        assert result is not None
        assert result.location.lat == 52.520008
        assert result.location.lon == 13.404954
        assert result.city == "Berlin"
        assert result.display_name == "Berlin, Germany"
        assert result.place_id == 12345
        assert result.boundingbox == [52.3, 52.7, 13.1, 13.7]
        assert result.cached is False
        assert result.timestamp is not None


@pytest.mark.asyncio
async def test_geocode_city_not_found():
    """Test geocoding when city is not found."""
    service = GeocodingService()

    with patch("httpx.AsyncClient") as mock_client:
        mock_response = MagicMock()
        mock_response.json.return_value = []  # No results
        mock_response.raise_for_status.return_value = None

        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        result = await service.geocode_city("NonExistentCity")

        assert result is None


@pytest.mark.asyncio
async def test_geocode_city_cache_hit():
    """Test that cached results are returned."""
    service = GeocodingService()

    # Mock HTTP response
    mock_response_data = [
        {
            "lat": "52.520008",
            "lon": "13.404954",
            "display_name": "Berlin, Germany",
            "place_id": "12345",
        }
    ]

    with patch("httpx.AsyncClient") as mock_client:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status.return_value = None

        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        # First call
        result1 = await service.geocode_city("Berlin")
        assert result1.cached is False

        # Second call should hit cache (no API call)
        result2 = await service.geocode_city("Berlin")

        assert result2.cached is True
        assert result1.location.lat == result2.location.lat
        assert result1.location.lon == result2.location.lon
        # API should only be called once
        assert mock_client.call_count == 1


@pytest.mark.asyncio
async def test_rate_limiting_in_service():
    """Test that rate limiting is enforced in service."""
    service = GeocodingService()

    mock_response_data = [
        {
            "lat": "52.520008",
            "lon": "13.404954",
            "display_name": "Berlin, Germany",
            "place_id": "12345",
        }
    ]

    with patch("httpx.AsyncClient") as mock_client:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status.return_value = None

        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        # Clear cache to ensure API calls
        service.cache._cache.clear()

        start_time = time.time()

        # Two different cities to avoid cache
        await service.geocode_city("Berlin")
        await service.geocode_city("London")

        elapsed = time.time() - start_time

        # Should take at least 1 second due to rate limiting
        assert elapsed >= 1.0


@pytest.mark.asyncio
async def test_user_agent_header():
    """Test that User-Agent header is properly set."""
    service = GeocodingService()

    mock_response_data = [
        {
            "lat": "52.520008",
            "lon": "13.404954",
            "display_name": "Berlin, Germany",
            "place_id": "12345",
        }
    ]

    with patch("httpx.AsyncClient") as mock_client:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status.return_value = None

        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        await service.geocode_city("Berlin")

        # Verify that get was called with proper headers including User-Agent
        mock_client_instance.get.assert_called_once()
        call_args = mock_client_instance.get.call_args
        assert "headers" in call_args.kwargs
        assert call_args.kwargs["headers"]["User-Agent"] == service.user_agent


@pytest.mark.asyncio
async def test_nominatim_api_error():
    """Test handling of Nominatim API errors."""
    service = GeocodingService()

    with patch("httpx.AsyncClient") as mock_client:
        mock_client_instance = AsyncMock()
        mock_client_instance.get.side_effect = httpx.HTTPStatusError(
            "API Error", request=None, response=MagicMock(status_code=503)
        )
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        with pytest.raises(Exception, match="Nominatim API HTTP error"):
            await service.geocode_city("Berlin")


@pytest.mark.asyncio
async def test_geocode_response_model_validation():
    """Test that response follows the correct Pydantic model."""
    service = GeocodingService()

    mock_response_data = [
        {
            "lat": "52.520008",
            "lon": "13.404954",
            "display_name": "Berlin, Germany",
            "place_id": "12345",
            "boundingbox": ["52.3", "52.7", "13.1", "13.7"],
        }
    ]

    with patch("httpx.AsyncClient") as mock_client:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status.return_value = None

        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        result = await service.geocode_city("Berlin")

        # Verify it's a proper GeocodingResponse
        assert isinstance(result, GeocodingResponse)
        assert isinstance(result.location, Location)
        assert isinstance(result.location.lat, float)
        assert isinstance(result.location.lon, float)
        assert isinstance(result.city, str)
        assert isinstance(result.display_name, str)
        assert isinstance(result.cached, bool)
        assert isinstance(result.timestamp, str)


@pytest.mark.asyncio
async def test_cache_integration():
    """Test that caching is properly integrated with the service."""
    service = GeocodingService()

    # Test that cache set/get works
    test_response = GeocodingResponse(
        city="TestCity",
        location=Location(lat=50.0, lon=10.0),
        display_name="Test City, Test Country",
        place_id=999,
        boundingbox=[49.9, 50.1, 9.9, 10.1],
        timestamp="2024-01-01T00:00:00+00:00",
        cached=False,
    )

    # Manually set cache
    service.cache.set("TestCity", test_response.model_dump())

    # Should return cached result without API call
    with patch("httpx.AsyncClient") as mock_api:
        result = await service.geocode_city("TestCity")

        assert result.cached is True
        assert result.city == "TestCity"
        assert result.location.lat == 50.0
        assert result.location.lon == 10.0
        # API should not be called
        mock_api.assert_not_called()


@pytest.mark.asyncio
async def test_service_initialization():
    """Test that service is properly initialized."""
    service = GeocodingService()

    # Check that components are initialized
    assert service.rate_limiter is not None
    assert service.cache is not None
    assert service.user_agent is not None
    assert "1.0" in service.user_agent  # Should contain version


@pytest.mark.asyncio
async def test_multiple_results_uses_first():
    """Test that service uses first result when multiple results returned."""
    service = GeocodingService()

    # Mock multiple results - HTTP API returns JSON array
    mock_response_data = [
        {
            "lat": "52.520008",
            "lon": "13.404954",
            "display_name": "Berlin, Germany",
            "place_id": "12345"
        },
        {
            "lat": "52.6",
            "lon": "13.5",
            "display_name": "Berlin, Other Country",
            "place_id": "67890"
        }
    ]

    with patch("httpx.AsyncClient") as mock_client:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status.return_value = None

        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        result = await service.geocode_city("Berlin")

        # Should use first result
        assert result.location.lat == 52.520008
        assert result.location.lon == 13.404954
        assert result.place_id == 12345

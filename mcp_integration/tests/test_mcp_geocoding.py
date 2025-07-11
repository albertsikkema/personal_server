"""
Tests for MCP Geocoding Tool.

This module contains comprehensive tests for the FastMCP geocoding tool,
including unit tests and integration tests with mocking.
"""

import json
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastmcp import Client

from mcp_integration.server import get_mcp_server, reset_mcp_server
from mcp_integration.tools.geocoding import _geocode_city_impl, reset_geocoding_service
from models.geocoding import GeocodingResponse, Location


class TestMCPGeocodingTool:
    """Test suite for the MCP geocoding tool."""

    def teardown_method(self):
        """Clean up after each test."""
        reset_mcp_server()
        reset_geocoding_service()

    @pytest.fixture
    def mcp_server(self):
        """Create a fresh MCP server for testing."""
        return get_mcp_server()

    @pytest.fixture
    def mcp_client(self, mcp_server):
        """Create an MCP client for testing."""
        return Client(mcp_server)

    @patch("mcp_integration.tools.geocoding.get_geocoding_service")
    async def test_geocode_city_success(self, mock_get_service, mcp_client):
        """Test successful geocoding via MCP tool."""
        # Mock service response
        mock_service = Mock()
        mock_service.geocode_city = AsyncMock(
            return_value=GeocodingResponse(
                city="London",
                location=Location(lat=51.5074, lon=-0.1278),
                display_name="London, Greater London, England, United Kingdom",
                place_id=12345,
                boundingbox=[51.2868, 51.6918, -0.5103, 0.3340],
                timestamp="2024-01-01T12:00:00+00:00",
                cached=False,
            )
        )
        mock_get_service.return_value = mock_service

        async with mcp_client:
            result = await mcp_client.call_tool("geocode_city", {"city": "London"})

            assert result is not None
            assert hasattr(result, "content")
            assert len(result.content) > 0
            assert result.content[0].text is not None

            # Parse the result
            result_data = json.loads(result.content[0].text)
            assert result_data["success"] is True
            assert result_data["city"] == "London"
            assert result_data["location"]["lat"] == 51.5074
            assert result_data["location"]["lon"] == -0.1278
            assert (
                result_data["display_name"]
                == "London, Greater London, England, United Kingdom"
            )
            assert result_data["place_id"] == 12345
            assert result_data["cached"] is False

    @patch("mcp_integration.tools.geocoding.get_geocoding_service")
    async def test_geocode_city_not_found(self, mock_get_service, mcp_client):
        """Test geocoding when city is not found."""
        mock_service = Mock()
        mock_service.geocode_city = AsyncMock(return_value=None)
        mock_get_service.return_value = mock_service

        async with mcp_client:
            result = await mcp_client.call_tool(
                "geocode_city", {"city": "NonexistentCity"}
            )

            assert result is not None
            assert hasattr(result, "content")
            assert len(result.content) > 0
            assert result.content[0].text is not None

            result_data = json.loads(result.content[0].text)
            assert "error" in result_data
            assert result_data["error"] == "City not found"
            assert result_data["city"] == "NonexistentCity"
            assert "message" in result_data

    @patch("mcp_integration.tools.geocoding.get_geocoding_service")
    async def test_geocode_city_service_error(self, mock_get_service, mcp_client):
        """Test geocoding when service throws an error."""
        mock_service = Mock()
        mock_service.geocode_city = AsyncMock(
            side_effect=Exception("Service unavailable")
        )
        mock_get_service.return_value = mock_service

        async with mcp_client:
            result = await mcp_client.call_tool("geocode_city", {"city": "London"})

            assert result is not None
            assert hasattr(result, "content")
            assert len(result.content) > 0
            assert result.content[0].text is not None

            result_data = json.loads(result.content[0].text)
            assert "error" in result_data
            assert result_data["error"] == "Geocoding service error"
            assert result_data["city"] == "London"
            assert "Service unavailable" in result_data["message"]

    async def test_geocode_city_empty_input(self, mcp_client):
        """Test geocoding with empty city name."""
        async with mcp_client:
            # This should raise a validation error due to FastMCP's validation
            with pytest.raises(
                (ValueError, TypeError)
            ):  # FastMCP raises validation error
                await mcp_client.call_tool("geocode_city", {"city": ""})

    async def test_geocode_city_whitespace_input(self, mcp_client):
        """Test geocoding with whitespace-only city name."""
        async with mcp_client:
            result = await mcp_client.call_tool("geocode_city", {"city": "   "})

            assert result is not None
            assert hasattr(result, "content")
            assert len(result.content) > 0
            assert result.content[0].text is not None

            result_data = json.loads(result.content[0].text)
            assert "error" in result_data
            assert result_data["error"] == "Invalid input"

    @patch("mcp_integration.tools.geocoding.get_geocoding_service")
    async def test_geocode_city_cached_result(self, mock_get_service, mcp_client):
        """Test geocoding with cached result."""
        mock_service = Mock()
        mock_service.geocode_city = AsyncMock(
            return_value=GeocodingResponse(
                city="Paris",
                location=Location(lat=48.8566, lon=2.3522),
                display_name="Paris, France",
                place_id=54321,
                boundingbox=[48.8155, 48.9021, 2.2247, 2.4697],
                timestamp="2024-01-01T12:00:00+00:00",
                cached=True,
            )
        )
        mock_get_service.return_value = mock_service

        async with mcp_client:
            result = await mcp_client.call_tool("geocode_city", {"city": "Paris"})

            assert result is not None
            assert hasattr(result, "content")
            assert len(result.content) > 0
            assert result.content[0].text is not None

            result_data = json.loads(result.content[0].text)
            assert result_data["success"] is True
            assert result_data["city"] == "Paris"
            assert result_data["cached"] is True

    async def test_mcp_server_tools_available(self, mcp_client):
        """Test that MCP server exposes the geocoding tool."""
        async with mcp_client:
            tools = await mcp_client.list_tools()

            assert tools is not None
            tool_names = [tool.name for tool in tools]
            assert "geocode_city" in tool_names

            # Check tool details
            geocoding_tool = next(
                (tool for tool in tools if tool.name == "geocode_city"), None
            )
            assert geocoding_tool is not None
            assert geocoding_tool.description is not None
            assert "city" in geocoding_tool.description.lower()
            assert "coordinates" in geocoding_tool.description.lower()

    async def test_mcp_server_info(self, mcp_client):
        """Test MCP server information."""
        async with mcp_client:
            # Test server is accessible and working
            tools = await mcp_client.list_tools()
            assert tools is not None

            # Verify server has the expected tools
            tool_names = [tool.name for tool in tools]
            assert "geocode_city" in tool_names


class TestMCPGeocodingToolDirect:
    """Direct tests for the geocoding tool function."""

    def teardown_method(self):
        """Clean up after each test."""
        reset_geocoding_service()

    @patch("mcp_integration.tools.geocoding.get_geocoding_service")
    async def test_geocode_city_function_success(self, mock_get_service):
        """Test the geocode_city function directly."""
        mock_service = Mock()
        mock_service.geocode_city = AsyncMock(
            return_value=GeocodingResponse(
                city="Berlin",
                location=Location(lat=52.5200, lon=13.4050),
                display_name="Berlin, Germany",
                place_id=98765,
                boundingbox=[52.3671, 52.6755, 13.0911, 13.7607],
                timestamp="2024-01-01T12:00:00+00:00",
                cached=False,
            )
        )
        mock_get_service.return_value = mock_service

        result = await _geocode_city_impl("Berlin")

        assert result["success"] is True
        assert result["city"] == "Berlin"
        assert result["location"]["lat"] == 52.5200
        assert result["location"]["lon"] == 13.4050

        # Verify service was called
        mock_service.geocode_city.assert_called_once_with("Berlin")

    @patch("mcp_integration.tools.geocoding.get_geocoding_service")
    async def test_geocode_city_function_not_found(self, mock_get_service):
        """Test the geocode_city function when city is not found."""
        mock_service = Mock()
        mock_service.geocode_city = AsyncMock(return_value=None)
        mock_get_service.return_value = mock_service

        result = await _geocode_city_impl("UnknownCity")

        assert "error" in result
        assert result["error"] == "City not found"
        assert result["city"] == "UnknownCity"

    async def test_geocode_city_function_empty_input(self):
        """Test the geocode_city function with empty input."""
        result = await _geocode_city_impl("")

        assert "error" in result
        assert result["error"] == "Invalid input"
        assert "City name cannot be empty" in result["message"]

    async def test_geocode_city_function_whitespace_trimming(self):
        """Test that the geocode_city function trims whitespace."""
        with patch(
            "mcp_integration.tools.geocoding.get_geocoding_service"
        ) as mock_get_service:
            mock_service = Mock()
            mock_service.geocode_city = AsyncMock(
                return_value=GeocodingResponse(
                    city="Tokyo",
                    location=Location(lat=35.6762, lon=139.6503),
                    display_name="Tokyo, Japan",
                    timestamp="2024-01-01T12:00:00+00:00",
                    cached=False,
                )
            )
            mock_get_service.return_value = mock_service

            result = await _geocode_city_impl("  Tokyo  ")

            # Verify service was called with trimmed input
            mock_service.geocode_city.assert_called_once_with("Tokyo")
            assert result["success"] is True

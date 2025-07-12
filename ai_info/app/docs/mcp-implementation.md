# MCP Integration Implementation Patterns

This document contains detailed implementation patterns for FastMCP server integration that exposes geocoding functionality through the Model Context Protocol, allowing LLM clients to access geocoding capabilities directly.

## FastMCP Server Overview
- **Location**: `mcp/server.py`
- **Tools**: `mcp/tools/geocoding.py`
- **Integration**: Mounted at `/mcp` in main FastAPI app
- **Transport**: Streamable HTTP

## MCP Tool Implementation Pattern

### Tool Definition with Type Safety

```python
# mcp/tools/geocoding.py
from typing import Annotated
from pydantic import Field
from fastmcp import FastMCP

mcp = FastMCP("GecodingTools")

@mcp.tool()
async def geocode_city(
    city: Annotated[str, Field(
        description="City name to geocode (1-200 characters)",
        min_length=1,
        max_length=200
    )]
) -> dict:
    """
    Geocode a city name to get its geographic coordinates.
    
    This tool converts city names to geographic coordinates using OpenStreetMap's
    Nominatim service. Results include latitude, longitude, display name, and
    optional bounding box information.
    """
    try:
        # Get geocoding service (reuse existing service)
        service = get_geocoding_service()
        
        # Perform geocoding
        result = await service.geocode_city(city.strip())
        
        if result is None:
            return {
                "error": "City not found",
                "city": city,
                "message": "No geocoding results found for the specified city"
            }
        
        # Convert to dict for MCP response
        response_dict = result.model_dump()
        response_dict["success"] = True
        
        return response_dict
        
    except Exception as e:
        return {
            "error": "Geocoding service error",
            "city": city,
            "message": str(e)
        }
```

## FastAPI Integration Pattern

### Lifespan Management with MCP

```python
# main.py additions
from contextlib import asynccontextmanager
from mcp.server import get_mcp_server

# Create MCP server and ASGI app
mcp_server = get_mcp_server()
mcp_app = mcp_server.http_app(path='/mcp')

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
    lifespan=lifespan,
)

# Mount MCP server
app.mount("/mcp", mcp_app)
```

## MCP Server Configuration Pattern

### Server Setup with Tool Registration

```python
# mcp/server.py
from fastmcp import FastMCP
from .tools.geocoding import geocode_city

# Global MCP server instance
_mcp_server = None

def get_mcp_server() -> FastMCP:
    """Get or create the MCP server instance."""
    global _mcp_server
    if _mcp_server is None:
        _mcp_server = FastMCP(
            name="FastAPI Geocoding MCP Server",
            instructions="""
            This server provides geocoding capabilities through the Model Context Protocol.
            Use the geocode_city tool to convert city names to geographic coordinates.
            """,
        )
        
        # Register the geocoding tool
        _mcp_server.add_tool(geocode_city)
    
    return _mcp_server
```

## Service Reuse Pattern

The MCP integration follows the principle of service reuse:

```python
# Singleton pattern for service management
_geocoding_service: Optional[GeocodingService] = None

def get_geocoding_service() -> GeocodingService:
    """Get or create the geocoding service instance."""
    global _geocoding_service
    if _geocoding_service is None:
        _geocoding_service = GeocodingService()
    return _geocoding_service
```

## Testing Pattern

### Unit Testing with Mocking

```python
# mcp/tests/test_mcp_geocoding.py
import pytest
from fastmcp import Client
from unittest.mock import Mock, patch, AsyncMock

class TestMCPGeocodingTool:
    @pytest.fixture
    def mcp_client(self):
        return Client(get_mcp_server())
    
    @patch('mcp.tools.geocoding.get_geocoding_service')
    async def test_geocode_city_success(self, mock_get_service, mcp_client):
        # Mock service response
        mock_service = Mock()
        mock_service.geocode_city = AsyncMock(return_value=GeocodingResponse(...))
        mock_get_service.return_value = mock_service
        
        async with mcp_client:
            result = await mcp_client.call_tool("geocode_city", {"city": "London"})
            result_data = json.loads(result[0].text)
            assert result_data["success"] is True
    
    @patch('mcp.tools.geocoding.get_geocoding_service')
    async def test_geocode_city_not_found(self, mock_get_service, mcp_client):
        # Mock service response for city not found
        mock_service = Mock()
        mock_service.geocode_city = AsyncMock(return_value=None)
        mock_get_service.return_value = mock_service
        
        async with mcp_client:
            result = await mcp_client.call_tool("geocode_city", {"city": "NonexistentCity"})
            result_data = json.loads(result[0].text)
            assert "error" in result_data
            assert result_data["error"] == "City not found"
    
    @patch('mcp.tools.geocoding.get_geocoding_service')
    async def test_geocode_city_service_error(self, mock_get_service, mcp_client):
        # Mock service error
        mock_service = Mock()
        mock_service.geocode_city = AsyncMock(side_effect=Exception("Service unavailable"))
        mock_get_service.return_value = mock_service
        
        async with mcp_client:
            result = await mcp_client.call_tool("geocode_city", {"city": "London"})
            result_data = json.loads(result[0].text)
            assert "error" in result_data
            assert result_data["error"] == "Geocoding service error"
```

## Key Design Principles

### 1. Service Reuse
MCP tools use identical services as REST API - no code duplication, same caching, rate limiting, and error handling.

### 2. Singleton Pattern
Single service instances shared across the application to ensure consistency and resource efficiency.

### 3. Proper Lifespan Management
MCP server lifecycle integrated with FastAPI using proper async context managers.

### 4. Error Handling
Structured error responses in MCP-compatible format with proper exception handling.

### 5. Testing
Comprehensive unit and integration tests with mocking to ensure reliability without external dependencies.

## Dependencies

```python
# pyproject.toml
dependencies = [
    "fastapi[standard]",
    "pydantic",
    "pydantic-settings",
    "uvicorn",
    "fastmcp",  # Added for MCP integration
]
```

## Development Commands

```bash
# Makefile additions for MCP testing

test-mcp:
	source venv/bin/activate && python -c "import asyncio; from fastmcp import Client; ..."

# Test MCP tools directly
test-mcp-tools:
	uv run python -m mcp.tests.test_mcp_geocoding
```

## Benefits of This Implementation

### 1. No Code Duplication
Reuses all existing geocoding logic including caching, rate limiting, and error handling.

### 2. Consistent Behavior
Same caching, rate limiting, and error handling between REST API and MCP interface.

### 3. Maintainable
Changes to geocoding service automatically reflected in MCP tools without additional code changes.

### 4. Follows Architecture
Maintains vertical slice pattern with MCP as separate module, following established project structure.

### 5. Easy to Extend
Can add more tools later (e.g., crawling tools) following the same pattern and conventions.

## Future Tool Extensions

### Crawling Tool Pattern
Following the same pattern, additional tools can be added:

```python
@mcp.tool()
async def crawl_url(
    url: Annotated[str, Field(description="URL to crawl")]
) -> dict:
    """Crawl a URL and return markdown content."""
    service = get_crawling_service()
    # Implementation following same pattern...
```

### Authentication Tool Pattern
```python
@mcp.tool()
async def verify_api_key(
    api_key: Annotated[str, Field(description="API key to verify")]
) -> dict:
    """Verify API key validity."""
    # Implementation following same pattern...
```

This modular approach ensures consistent patterns and easy maintenance across all MCP tools.
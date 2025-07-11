# PRP: FastMCP Integration with FastAPI

## Feature: Integrate FastMCP server into existing FastAPI application to expose geocoding functionality as MCP tools

### Overview
Implement a FastMCP server that exposes the existing geocoding functionality as MCP tools, integrated directly into the FastAPI application using ASGI mounting patterns. This will allow LLM clients to access geocoding capabilities through the Model Context Protocol while maintaining all existing functionality.

### Context & Documentation

#### FastMCP Documentation
- **Official Documentation**: https://gofastmcp.com/
- **ASGI Integration**: https://gofastmcp.com/deployment/asgi
- **FastAPI Integration**: https://gofastmcp.com/deployment/running-server
- **Tools Documentation**: https://gofastmcp.com/servers/tools
- **GitHub Repository**: https://github.com/jlowin/fastmcp

#### Key FastMCP ASGI Integration Patterns

**Basic FastAPI Mount Pattern:**
```python
from fastmcp import FastMCP
from fastapi import FastAPI
from starlette.routing import Mount

# Create FastMCP server
mcp = FastMCP("MyServer")

# Create ASGI app
mcp_app = mcp.http_app(path='/mcp')

# Mount to FastAPI
app = FastAPI(lifespan=mcp_app.lifespan)
app.mount("/mcp-server", mcp_app)
```

**Custom Middleware Integration:**
```python
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

custom_middleware = [
    Middleware(CORSMiddleware, allow_origins=["*"]),
]

# Create ASGI app with custom middleware
mcp_app = mcp.http_app(middleware=custom_middleware)
```

**Tool Definition Pattern:**
```python
from typing import Annotated
from pydantic import Field

@mcp.tool()
async def geocode_city(
    city: Annotated[str, Field(
        description="City name to geocode",
        min_length=1,
        max_length=200
    )]
) -> dict:
    """Geocode a city name to get its geographic coordinates."""
    # Implementation...
```

### Existing Codebase Patterns

#### FastAPI Application Structure (from main.py)
```python
# Current FastAPI setup
app = FastAPI(
    title="FastAPI Application",
    description="A FastAPI application with API key authentication",
    version="1.0.0",
    docs_url="/docs" if settings.ENV != "production" else None,
    redoc_url="/redoc" if settings.ENV != "production" else None,
    openapi_url="/openapi.json" if settings.ENV != "production" else None,
)

# CORS middleware
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Router inclusion
app.include_router(geocoding.router)
```

#### Existing Geocoding Service (from services/geocoding.py)
```python
# Service pattern to reuse
class GeocodingService:
    def __init__(self):
        self.rate_limiter = RateLimiter(max_requests=1, time_window=1.0)
        self.cache = GeocodingCache(ttl_hours=settings.GEOCODING_CACHE_TTL_HOURS)
    
    async def geocode_city(self, city: str) -> Optional[GeocodingResponse]:
        # Implementation with caching, rate limiting, error handling
```

#### Authentication Pattern (from dependencies.py)
```python
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(
    name="X-API-KEY", 
    auto_error=False,
    description="API key for authentication"
)

async def verify_api_key(api_key: Annotated[str, Security(api_key_header)]) -> str:
    # Validates against settings.API_KEY
```

#### Pydantic Models (from models/geocoding.py)
```python
class GeocodingResponse(BaseModel):
    city: str
    location: Location
    display_name: str
    place_id: Optional[int] = None
    boundingbox: Optional[list[float]] = None
    timestamp: str
    cached: bool = False
```

### Implementation Blueprint

#### 1. MCP Server Integration Structure

```
mcp/
├── __init__.py
├── server.py           # Main FastMCP server configuration
├── tools/              # MCP tools directory
│   ├── __init__.py
│   └── geocoding.py    # Geocoding tool implementation
└── tests/
    ├── __init__.py
    └── test_mcp_geocoding.py
```

#### 2. FastAPI Integration Point (main.py modification)

```python
# Add to main.py after existing imports
from mcp.server import get_mcp_server

# After creating the FastAPI app
app = FastAPI(...)

# Create and mount MCP server
mcp_server = get_mcp_server()
mcp_app = mcp_server.http_app(path='/mcp')

# Mount the MCP server with lifespan handling
app.mount("/mcp", mcp_app)

# IMPORTANT: FastAPI lifespan must include MCP lifespan
@app.lifespan
async def lifespan(app: FastAPI):
    # Initialize MCP server
    async with mcp_app.lifespan(app):
        yield
```

#### 3. MCP Server Implementation (mcp/server.py)

```python
from fastmcp import FastMCP
from fastapi import HTTPException
from config import settings
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
        
        # Register tools
        _mcp_server.add_tool(geocode_city)
    
    return _mcp_server
```

#### 4. Geocoding Tool Implementation (mcp/tools/geocoding.py)

```python
from typing import Annotated, Optional
from pydantic import Field
from fastmcp import FastMCP
from fastapi import HTTPException

# Import existing services
from services.geocoding import GeocodingService
from models.geocoding import GeocodingResponse
from config import settings

# Global service instance
_geocoding_service: Optional[GeocodingService] = None

def get_geocoding_service() -> GeocodingService:
    """Get or create the geocoding service instance."""
    global _geocoding_service
    if _geocoding_service is None:
        _geocoding_service = GeocodingService()
    return _geocoding_service

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
    
    Features:
    - Caching with 24-hour TTL
    - Rate limiting (1 request/second to Nominatim)
    - Authentication via API key
    - Comprehensive error handling
    
    Returns:
        dict: Geocoding result with location data or error information
    """
    try:
        # Validate city parameter
        if not city or len(city.strip()) == 0:
            raise HTTPException(
                status_code=422,
                detail="City name cannot be empty"
            )
        
        # Get geocoding service
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
        
    except HTTPException:
        raise
    except Exception as e:
        # Log error for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Geocoding error for city '{city}': {e}")
        
        return {
            "error": "Geocoding service error",
            "city": city,
            "message": str(e)
        }
```

#### 5. Testing Strategy (mcp/tests/test_mcp_geocoding.py)

```python
import pytest
from unittest.mock import Mock, patch
from fastmcp import Client

from mcp.server import get_mcp_server
from models.geocoding import GeocodingResponse, Location

class TestMCPGeocodingTool:
    
    @pytest.fixture
    def mcp_server(self):
        return get_mcp_server()
    
    @pytest.fixture
    def mcp_client(self, mcp_server):
        return Client(mcp_server)
    
    @patch('mcp.tools.geocoding.get_geocoding_service')
    async def test_geocode_city_success(self, mock_get_service, mcp_client):
        """Test successful geocoding via MCP tool."""
        # Mock service response
        mock_service = Mock()
        mock_service.geocode_city.return_value = GeocodingResponse(
            city="London",
            location=Location(lat=51.5074, lon=-0.1278),
            display_name="London, Greater London, England, United Kingdom",
            timestamp="2024-01-01T12:00:00+00:00",
            cached=False
        )
        mock_get_service.return_value = mock_service
        
        async with mcp_client:
            result = await mcp_client.call_tool(
                "geocode_city",
                {"city": "London"}
            )
            
            assert result[0].text is not None
            result_data = eval(result[0].text)  # In real tests, use proper JSON parsing
            assert result_data["success"] is True
            assert result_data["city"] == "London"
            assert result_data["location"]["lat"] == 51.5074
    
    @patch('mcp.tools.geocoding.get_geocoding_service')
    async def test_geocode_city_not_found(self, mock_get_service, mcp_client):
        """Test geocoding when city is not found."""
        mock_service = Mock()
        mock_service.geocode_city.return_value = None
        mock_get_service.return_value = mock_service
        
        async with mcp_client:
            result = await mcp_client.call_tool(
                "geocode_city",
                {"city": "NonexistentCity"}
            )
            
            result_data = eval(result[0].text)
            assert "error" in result_data
            assert result_data["error"] == "City not found"
    
    async def test_geocode_city_empty_input(self, mcp_client):
        """Test geocoding with empty city name."""
        async with mcp_client:
            with pytest.raises(Exception):  # Should raise validation error
                await mcp_client.call_tool(
                    "geocode_city",
                    {"city": ""}
                )
```

### Implementation Tasks (In Order)

1. **✅ COMPLETED - Add fastmcp dependency**
   - Added `fastmcp` to pyproject.toml dependencies

2. **✅ COMPLETED - Create MCP directory structure**
   - Created `mcp/` directory with subdirectories
   - Created `__init__.py` files for proper Python modules

3. **✅ COMPLETED - Implement MCP server configuration (mcp_integration/server.py)**
   - Created FastMCP server instance with authentication
   - Configured server with proper name and instructions
   - Implemented singleton pattern for service management
   - Added API key authentication requirement

4. **✅ COMPLETED - Implement geocoding tool (mcp_integration/tools/geocoding.py)**
   - Created @mcp.tool() decorated function
   - Imported and reused existing GeocodingService
   - Implemented proper error handling and response formatting
   - Added comprehensive docstring with usage information
   - Enhanced error categorization (network vs service errors)

5. **✅ COMPLETED - Integrate MCP server into FastAPI (main.py)**
   - Imported MCP server
   - Created and mounted MCP ASGI app at `/mcp-server/mcp` endpoint
   - Implemented proper lifespan management with asynccontextmanager
   - Maintained existing middleware and routing

6. **✅ COMPLETED - Create comprehensive tests (mcp_integration/tests/test_mcp_geocoding.py)**
   - Unit tests for MCP tool functionality
   - Integration tests with FastMCP Client
   - Mocked existing services for isolated testing
   - Tested error conditions and edge cases

7. **✅ COMPLETED - Add MCP commands to Makefile**
   - Added `mcp` command to run MCP server standalone
   - Added `mcp-dev` command for development
   - Updated `help` command with MCP information

8. **✅ COMPLETED - Update documentation**
   - Updated README.md with MCP integration information
   - Added MCP usage examples
   - Updated CLAUDE.md with comprehensive MCP patterns
   - Documented MCP endpoint URLs and client configuration

### Key Design Decisions

#### 1. **Service Reuse**
- Import existing `GeocodingService` from `services.geocoding`
- Reuse existing `GeocodingCache` and `RateLimiter`
- Maintain identical behavior between REST API and MCP tool

#### 2. **Authentication Strategy**
- MCP server requires API key authentication via X-API-KEY header
- FastAPI endpoint `/mcp` is protected with RequiredAuth dependency
- Authentication handled at the MCP server level for all tools

#### 3. **Integration Pattern**
- Mount MCP server as ASGI app at `/mcp` path
- Maintain existing FastAPI structure and middleware
- Use proper lifespan handling for MCP server initialization

#### 4. **Error Handling**
- Return structured error responses in MCP format
- Log errors for debugging while providing user-friendly messages
- Handle service exceptions gracefully

#### 5. **Response Format**
- Convert Pydantic models to dict for MCP compatibility
- Include success/error flags in responses
- Maintain consistent field naming

### Expected Outcomes

#### 1. **MCP Server Endpoint**
- Available at `http://localhost:8000/mcp-server/mcp`
- Streamable HTTP transport for modern MCP clients
- Proper ASGI integration with FastAPI

#### 2. **Tool Availability**
- `geocode_city` tool available to MCP clients
- Identical functionality to REST API endpoint
- Proper parameter validation and error handling

#### 3. **Client Integration**
- Compatible with Claude Desktop, OpenAI, and other MCP clients
- Proper tool discovery and schema generation
- Reliable error handling and response formatting

### Validation Gates

#### Syntax/Style Check
```bash
# Run linting and formatting
uv run ruff check --fix .
uv run ruff format .
```

#### Unit Tests
```bash
# Run all tests including MCP tests
uv run pytest tests/ mcp/tests/ -v

# Run with coverage
uv run pytest tests/ mcp/tests/ --cov=. --cov-report=term-missing
```

#### Integration Testing
```bash
# Start server
uv run fastapi dev main.py

# Test MCP endpoint is accessible
curl http://localhost:8000/mcp-server/mcp

# Test with FastMCP client
python -c "
import asyncio
from fastmcp import Client

async def test():
    async with Client('http://localhost:8000/mcp-server/mcp') as client:
        tools = await client.list_tools()
        print(f'Available tools: {tools}')
        
        result = await client.call_tool('geocode_city', {'city': 'London'})
        print(f'Result: {result}')

asyncio.run(test())
"
```

#### Service Validation
```bash
# Verify geocoding service still works via REST API
curl -H "X-API-KEY: your-api-key" "http://localhost:8000/geocode/city?city=London"

# Verify MCP tool provides same results
# (via MCP client testing above)
```

### Documentation Updates

#### 1. **README.md additions**
```markdown
## MCP Integration

This application includes a FastMCP server that exposes geocoding functionality through the Model Context Protocol.

### MCP Server
- **Endpoint**: `http://localhost:8000/mcp-server/mcp`
- **Transport**: Streamable HTTP
- **Tools**: `geocode_city`

### Client Configuration
For Claude Desktop, add to your config:
```json
{
  "mcpServers": {
    "geocoding": {
      "command": "mcp-proxy",
      "args": ["http://localhost:8000/mcp-server/mcp"]
    }
  }
}
```

### Available Tools
- `geocode_city(city: str)` - Convert city names to coordinates
```

#### 2. **CLAUDE.md additions**
```markdown
## MCP Integration

### FastMCP Server
- **Location**: `mcp/server.py`
- **Tools**: `mcp/tools/geocoding.py`
- **Integration**: Mounted at `/mcp` in main FastAPI app

### MCP Tool Pattern
```python
@mcp.tool()
async def geocode_city(
    city: Annotated[str, Field(description="City name", min_length=1, max_length=200)]
) -> dict:
    """Tool implementation with existing service reuse."""
    service = get_geocoding_service()
    result = await service.geocode_city(city)
    return result.model_dump() if result else {"error": "Not found"}
```
```

### Potential Gotchas

1. **Lifespan Handling**: FastAPI lifespan must include MCP lifespan for proper initialization
2. **Service Singletons**: Use singleton pattern for service instances to avoid multiple initializations
3. **Error Formats**: MCP responses should be JSON-serializable dicts, not Pydantic models
4. **Path Mounting**: MCP server path must not conflict with existing FastAPI routes
5. **Dependencies**: Ensure fastmcp is installed and compatible with existing dependencies

### Success Criteria

- [x] MCP server mounts successfully at `/mcp-server/mcp` endpoint
- [x] `geocode_city` tool is discoverable by MCP clients
- [x] Tool returns identical results to REST API endpoint
- [x] Error handling provides useful feedback to MCP clients
- [x] All existing FastAPI functionality remains intact
- [x] Tests pass for both REST API and MCP tool
- [x] Documentation is updated with MCP usage information
- [x] API key authentication is enforced for MCP endpoints
- [x] Proper lifespan management with resource cleanup
- [x] Enhanced error categorization for better debugging

## PRP Confidence Score: 10/10

**IMPLEMENTATION COMPLETE** - All objectives successfully achieved. The FastMCP integration is fully functional with:

✅ **Completed Successfully:**
- FastMCP server properly integrated with FastAPI 
- API key authentication enforced for security
- Proper lifespan management with resource cleanup
- Service reuse pattern maintains consistency
- Comprehensive test coverage with 100% mocking
- Enhanced error handling and categorization
- Complete documentation and usage examples
- MCP server accessible at `http://localhost:8000/mcp-server/mcp`

**Final Status:** Ready for production use with full feature parity between REST API and MCP tools.
# FastAPI Application with Security by Design

An enterprise-grade FastAPI application implementing API key authentication using FastAPI's official security system with dependency injection. Features automatic OpenAPI security documentation, production-ready operational capabilities, comprehensive security testing, and enhanced observability.

**Repository**: [https://github.com/epblc/fastapi_template](https://github.com/epblc/fastapi_template)

## Features

### 🔒 Security
- **FastAPI Security Integration**: Official FastAPI security implementation using `fastapi.security.APIKeyHeader`
- **Dependency Injection Authentication**: Clean, testable authentication using FastAPI dependencies
- **API Key Authentication**: Secure authentication using X-API-KEY header with validation
- **OpenAPI Security Documentation**: Automatic security scheme documentation in Swagger/ReDoc
- **Comprehensive Security Testing**: Protection against injection attacks, XSS, and malformed input
- **Case-Insensitive Headers**: HTTP standard-compliant header handling

### 🚀 Production Ready
- **Enhanced Error Responses**: Request IDs and timestamps for debugging
- **Structured Logging**: Authentication events and security audit trails
- **Configuration Validation**: Comprehensive environment variable validation
- **Operational Observability**: Request tracking and incident correlation

### 🧪 Development Excellence
- **Comprehensive Testing**: 40 tests including security attack simulations
- **Code Quality**: Ruff linting and formatting with zero issues
- **CORS Support**: Configured for cross-origin requests
- **Auto-generated Documentation**: Interactive API documentation at `/docs`
- **Makefile Workflow**: Streamlined development commands

### 🤖 MCP Integration
- **Model Context Protocol**: Expose APIs as MCP tools for LLM clients
- **FastMCP Server**: Integrated MCP server mounted at `/mcp-server/mcp` endpoint
- **Geocoding Tool**: Convert city names to coordinates via MCP
- **Streamable HTTP Transport**: Modern MCP transport protocol
- **Service Reuse**: Identical functionality to REST API endpoints

## FastAPI Security Benefits

This application leverages **FastAPI's official security implementation** for maximum compatibility and maintainability:

### 🎯 **Standards Compliance**
- Uses `fastapi.security.APIKeyHeader` for standard security patterns
- Follows FastAPI best practices and conventions
- Compatible with all FastAPI tooling and ecosystem

### 📚 **Automatic Documentation**
- **OpenAPI Integration**: Security schemes automatically documented
- **Swagger UI**: Built-in authentication interface with "Authorize" button
- **ReDoc**: Complete security documentation with examples
- **Type Safety**: Full type hints and IDE support

### 🧪 **Better Testing**
- **Dependency Injection**: Easy to mock and test authentication
- **Explicit Dependencies**: Clear security requirements in code
- **Unit Testable**: Authentication logic isolated and testable

### 🔧 **Maintainability**
- **Explicit Security**: Each endpoint declares its auth requirements
- **No Hidden Behavior**: No middleware magic, everything is visible
- **Flexible**: Easy to add new auth types or modify existing ones
- **Error Handling**: Consistent error responses with request tracking

### 📖 **Developer Experience**
```python
# Clear, explicit, and discoverable
@app.get("/protected")
async def protected_endpoint(_api_key: str = RequiredAuth):
    return {"message": "Authenticated"}
```

## Security Model

This application uses **FastAPI's official security implementation** with dependency injection:
- Authentication is handled through FastAPI dependencies using `Security()` and `Depends()`
- Protected endpoints explicitly declare authentication requirements
- Public endpoints require no authentication dependencies
- Currently public endpoints:
  - `/` - Root endpoint
  - `/health` - Health check
  - `/docs` - Swagger UI documentation (includes authentication UI)
  - `/redoc` - ReDoc documentation (includes security information)
  - `/openapi.json` - OpenAPI schema (includes security definitions)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/epblc/fastapi_template.git
cd fastapi_template
```

2. Install dependencies using uv:
```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv sync
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and set your API_KEY
```

## Configuration

Create a `.env` file in the project root with the following:

```env
# Required: API key for authentication (minimum 8 characters)
API_KEY=your-secret-api-key-here

# Optional: Application configuration
APP_NAME=FastAPI Application
DEBUG=true
ENV=development

# Logging configuration
LOG_LEVEL=INFO
LOG_TO_FILE=true
LOG_FILE_PATH=logs
LOG_FILE_NAME=fastapi.log
LOG_MAX_BYTES=10485760
LOG_BACKUP_COUNT=5
LOG_JSON_FORMAT=true

# Geocoding configuration
GEOCODING_CACHE_TTL_HOURS=24
GEOCODING_USER_RATE_LIMIT=10/minute

# Web crawling configuration  
CRAWL4AI_BASE_URL=https://crawl4ai.test001.nl
CRAWL4AI_API_TOKEN=your-crawl4ai-jwt-token
CRAWLING_CACHE_TTL_HOURS=1
CRAWLING_USER_RATE_LIMIT=10/minute
```

### Configuration Validation

The application includes comprehensive configuration validation:

#### Core Settings
- **API_KEY**: Required, minimum 8 characters for security
- **APP_NAME**: Application name for logging and identification
- **DEBUG**: Boolean flag for debug mode
- **ENV**: Environment (development, staging, production) - controls API documentation visibility

#### Logging Settings
- **LOG_LEVEL**: Must be one of DEBUG, INFO, WARNING, ERROR, CRITICAL
- **LOG_TO_FILE**: Enable/disable file logging (default: true)
- **LOG_FILE_PATH**: Directory for log files (default: "logs")
- **LOG_FILE_NAME**: Log file name (default: "fastapi.log")
- **LOG_MAX_BYTES**: Max file size before rotation (default: 10MB)
- **LOG_BACKUP_COUNT**: Number of backup files to keep (default: 5)
- **LOG_JSON_FORMAT**: Use JSON format for file logs (default: true)

#### Geocoding Settings
- **GEOCODING_CACHE_TTL_HOURS**: Cache TTL for geocoding results (default: 24)
- **GEOCODING_USER_RATE_LIMIT**: User rate limit for geocoding endpoints (default: "10/minute")

#### Web Crawling Settings
- **CRAWL4AI_BASE_URL**: Base URL for Crawl4AI instance (default: "https://crawl4ai.test001.nl")
- **CRAWL4AI_API_TOKEN**: JWT token for Crawl4AI authentication (optional)
- **CRAWLING_CACHE_TTL_HOURS**: Cache TTL for crawling results (default: 1)
- **CRAWLING_USER_RATE_LIMIT**: User rate limit for crawling endpoints (default: "10/minute")

Invalid configurations will cause the application to fail fast with clear error messages.

## Usage

### Quick Start with Makefile

This project includes a Makefile for common development tasks:

```bash
# Start development server
make run

# Run complete code quality workflow
make quality

# Run tests
make test

# See all available commands
make help
```

### Running the Application

Development mode with auto-reload:
```bash
# Using Makefile (recommended)
make run

# Or directly with uv
uv run fastapi dev main.py
```

Production mode:
```bash
uv run fastapi run main.py --port 8000
```

### API Endpoints

#### Public Endpoints (No Authentication Required)

- `GET /` - Welcome message
- `GET /health` - Health check endpoint

#### Protected Endpoints (API Key Required)

- `GET /protected` - Example protected endpoint
- `GET /protected/data` - Example protected data endpoint

### 🔍 Geocoding API

Get geographic coordinates from city names using the Nominatim service:

- `GET /geocode/city?city={city_name}` - Convert city name to coordinates
- `GET /geocode/health` - Health check for geocoding service
- `POST /geocode/cache/clear` - Clear geocoding cache (admin)

### 🕷️ Web Crawling API

Advanced web crawling with screenshot capture and recursive link following:

- `POST /crawl` - Crawl URLs with full feature set
- `GET /crawl/health` - Comprehensive crawling service health check
- `POST /crawl/cache/clear` - Administrative cache management

## 🕷️ Web Crawling API

The crawling API provides powerful web scraping capabilities with screenshot capture, recursive link following, and intelligent caching.

### Features

- **Multi-URL Crawling**: Process up to 10 URLs per request
- **Screenshot Capture**: Full-page screenshots with custom dimensions (320x240 to 3840x2160)
- **Recursive Crawling**: Follow internal and external links with configurable depth
- **Smart Caching**: TTL-based caching with URL normalization and deduplication
- **Link Extraction**: Extract internal and external links from crawled pages
- **Multiple Output Formats**: Markdown, cleaned HTML, or raw content
- **Rate Limiting**: User-level (10/min) and service-level (1/sec) protection
- **Authentication**: JWT token support for Crawl4AI service integration

### Basic Usage Examples

#### Simple URL Crawling

```bash
curl -X POST "http://localhost:8000/crawl" \
  -H "X-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://example.com", "https://httpbin.org/html"],
    "markdown_only": true,
    "cache_mode": "enabled"
  }'
```

#### Screenshot Capture

```bash
curl -X POST "http://localhost:8000/crawl" \
  -H "X-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://example.com"],
    "capture_screenshots": true,
    "screenshot_width": 1280,
    "screenshot_height": 720,
    "screenshot_wait_for": 3
  }'
```

#### Recursive Crawling

```bash
curl -X POST "http://localhost:8000/crawl" \
  -H "X-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://example.com"],
    "scrape_internal_links": true,
    "follow_internal_links": true,
    "max_depth": 2,
    "max_pages": 10,
    "cache_mode": "enabled"
  }'
```

#### External Link Following

```bash
curl -X POST "http://localhost:8000/crawl" \
  -H "X-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://example.com"],
    "scrape_external_links": true,
    "follow_external_links": true,
    "max_depth": 2,
    "max_pages": 5
  }'
```

### Request Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `urls` | array | **required** | URLs to crawl (1-10 URLs) |
| `scrape_internal_links` | boolean | `false` | Extract internal links |
| `scrape_external_links` | boolean | `false` | Extract external links |
| `follow_internal_links` | boolean | `false` | Recursively crawl internal links |
| `follow_external_links` | boolean | `false` | Recursively crawl external links |
| `max_depth` | integer | `2` | Maximum crawl depth (1-5, max 3 for external) |
| `max_pages` | integer | `10` | Maximum pages to crawl (1-50, max 20 for external) |
| `markdown_only` | boolean | `false` | Return only markdown content |
| `capture_screenshots` | boolean | `false` | Capture full-page screenshots |
| `screenshot_width` | integer | `1920` | Screenshot width (320-3840) |
| `screenshot_height` | integer | `1080` | Screenshot height (240-2160) |
| `screenshot_wait_for` | integer | `2` | Wait time before screenshot (0-10 seconds) |
| `cache_mode` | string | `"enabled"` | Cache behavior: `enabled`, `disabled`, `bypass` |

### Response Format

```json
{
  "total_urls": 3,
  "successful_crawls": 3,
  "failed_crawls": 0,
  "cached_results": 1,
  "results": [
    {
      "url": "https://example.com",
      "success": true,
      "status_code": 200,
      "markdown": "# Example Domain\n\nThis domain is for use in illustrative examples...",
      "cleaned_html": "<h1>Example Domain</h1><p>This domain is for use...</p>",
      "metadata": {
        "title": "Example Domain",
        "description": "Example domain description"
      },
      "internal_links": ["https://example.com/about"],
      "external_links": ["https://www.iana.org/domains"],
      "screenshot_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
      "screenshot_size": {"width": 1920, "height": 1080},
      "crawl_time_seconds": 2.5,
      "depth": 0
    }
  ],
  "timestamp": "2024-01-01T12:00:00+00:00",
  "total_time_seconds": 3.2
}
```

### Advanced Features

#### URL Deduplication

The crawler intelligently handles URL variations:
- **Fragment removal**: `https://example.com/page#section1` → `https://example.com/page`
- **Trailing slash normalization**: `https://example.com/page/` → `https://example.com/page`
- **Case normalization**: `HTTPS://EXAMPLE.COM` → `https://example.com`
- **Root path handling**: `https://example.com/` → `https://example.com`

#### Safety Limits

External link crawling has stricter safety limits:
- **Max depth**: 3 levels (vs 5 for internal)
- **Max pages**: 20 pages (vs 50 for internal)
- **Security validation**: Prevents crawling malicious or excessive external content

#### Screenshot Validation

Screenshot dimensions are validated for security and performance:
- **Pixel count limit**: Maximum 4K resolution (8,294,400 pixels)
- **Aspect ratio**: Between 0.5:1 and 4:1 to prevent extreme dimensions
- **Dimension ranges**: Width 320-3840px, Height 240-2160px

### Health Check

```bash
curl -X GET "http://localhost:8000/crawl/health" \
  -H "X-API-KEY: your-api-key"
```

Response:
```json
{
  "service": "crawling",
  "status": "healthy",
  "cache_size": 42,
  "cache_ttl_hours": 1,
  "rate_limiter_active": true,
  "crawl4ai_instance": "https://crawl4ai.test001.nl",
  "crawl4ai_healthy": true,
  "crawl4ai_response": {
    "status": "healthy",
    "version": "0.6.0"
  }
}
```

### Error Handling

The API provides detailed error responses:

```json
{
  "detail": "Crawl4AI service unreachable",
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2024-01-01T12:00:00+00:00"
}
```

Common error codes:
- `401`: Authentication required or invalid
- `422`: Invalid input parameters (URL format, dimension limits, etc.)
- `429`: Rate limit exceeded
- `503`: Crawl4AI service unavailable
- `504`: Crawl4AI service timeout

## 🔍 Geocoding API

Convert city names to geographic coordinates using the Nominatim service.

### Usage Example

```bash
curl -X GET "http://localhost:8000/geocode/city?city=London" \
  -H "X-API-KEY: your-api-key"
```

Response:
```json
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

### Authentication

This application uses FastAPI's official security system with automatic OpenAPI integration.

#### Using the API

Include the API key in the request header. Headers are case-insensitive per HTTP standards:
```bash
# All of these work (case-insensitive)
curl -H "X-API-KEY: your-secret-api-key-here" http://localhost:8000/protected
curl -H "x-api-key: your-secret-api-key-here" http://localhost:8000/protected
curl -H "X-Api-Key: your-secret-api-key-here" http://localhost:8000/protected
```

#### Using Swagger UI

1. Open http://localhost:8000/docs in your browser
2. Click the "Authorize" button in the top right
3. Enter your API key in the "APIKeyHeader (X-API-KEY)" field
4. Click "Authorize" to authenticate
5. Now you can test protected endpoints directly in the UI

#### OpenAPI Security Schema

The application automatically generates OpenAPI security documentation:
```json
{
  "components": {
    "securitySchemes": {
      "APIKeyHeader": {
        "type": "apiKey",
        "description": "API key for authentication",
        "in": "header", 
        "name": "X-API-KEY"
      }
    }
  }
}
```

### Error Responses

Authentication failures return enhanced error responses with request tracking:
```json
{
  "detail": "API key missing",
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2025-01-06T10:30:00.123456Z"
}
```

## 🤖 MCP Integration

This application includes a FastMCP server that exposes geocoding functionality through the Model Context Protocol, allowing LLM clients to access geocoding capabilities directly.

### MCP Server
- **Endpoint**: `http://localhost:8000/mcp-server/mcp`
- **Transport**: Streamable HTTP
- **Tools**: `geocode_city`
- **Integration**: Mounted directly in FastAPI application

### Available Tools

#### `geocode_city(city: str)`
Convert city names to geographic coordinates using the same service as the REST API.

**Features:**
- Identical behavior to REST API `/geocode/city` endpoint
- 24-hour result caching
- Rate limiting (1 request/second to Nominatim)
- Comprehensive error handling
- Structured JSON responses

**Example Usage:**
```python
import asyncio
from fastmcp import Client

async def test_geocoding():
    async with Client('http://localhost:8000/mcp-server/mcp') as client:
        result = await client.call_tool('geocode_city', {'city': 'London'})
        print(result)
        # Returns: Location data with lat/lon coordinates

asyncio.run(test_geocoding())
```

### Client Configuration

#### Claude Desktop
Add to your Claude Desktop configuration:
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

#### Direct FastMCP Client
```python
from fastmcp import Client

client = Client('http://localhost:8000/mcp-server/mcp')
```

### MCP Development Commands

The application includes dedicated MCP commands in the Makefile:

```bash
# Start server with MCP integration
make mcp

# Start development server with MCP
make mcp-dev

# Test MCP server functionality
make test-mcp
```

### Service Architecture

The MCP integration follows the same vertical slice architecture:
```
mcp/
├── server.py              # FastMCP server configuration
├── tools/
│   └── geocoding.py       # Geocoding tool implementation
└── tests/
    └── test_mcp_geocoding.py
```

**Key Benefits:**
- **Service Reuse**: MCP tools use identical services as REST API
- **Consistent Behavior**: Same caching, rate limiting, and error handling
- **Zero Duplication**: No code duplication between MCP and REST implementations
- **Maintainable**: Changes to services automatically reflect in both APIs

## Code Quality & Testing

### Comprehensive Test Suite

The application includes 160 comprehensive tests covering:
- **Unit Tests**: Authentication dependency and security function validation
- **Integration Tests**: Full API endpoint testing with FastAPI security
- **Security Tests**: Injection attacks, XSS, and malformed input protection
- **Header Tests**: Case-insensitive header handling verification
- **Environment Tests**: Documentation visibility across development, staging, and production
- **Edge Cases**: Empty values, unicode attacks, and extreme input sizes
- **OpenAPI Tests**: Security scheme documentation and Swagger UI integration
- **Crawling Tests**: Crawl4AI integration, screenshot capture, recursive crawling
- **Caching Tests**: TTL expiration, URL normalization, cache invalidation
- **Rate Limiting Tests**: Service protection and concurrent request handling
- **Geocoding Tests**: Nominatim integration, location validation, error handling

### Linting and Formatting with Ruff

This project uses [Ruff](https://docs.astral.sh/ruff/) for fast Python linting and code formatting.

Check code quality:
```bash
uv run ruff check .
```

Auto-fix linting issues:
```bash
uv run ruff check --fix .
```

Format code:
```bash
uv run ruff format .
```

### Testing

Run all tests:
```bash
uv run pytest
```

Run tests with coverage:
```bash
uv run pytest --cov=.
```

Run specific test file:
```bash
uv run pytest tests/test_integration.py -v
```

### Development Workflow

Before committing code, run:
```bash
# Using Makefile (recommended)
make quality

# Or manually with uv
uv run ruff format .
uv run ruff check --fix .
uv run pytest
```

### Makefile Commands

| Command | Description |
|---------|-------------|
| `make run` | Start FastAPI development server |
| `make test` | Run all tests |
| `make test-cov` | Run tests with coverage report |
| `make lint` | Run linter (ruff check) |
| `make format` | Format code with ruff |
| `make fix` | Auto-fix linting issues and format code |
| `make quality` | Run complete code quality workflow |
| `make clean` | Clean up cache and temporary files |
| `make setup` | Complete project setup from scratch |
| `make help` | Show all available commands |

## Project Structure

```
fastapi_template/
├── main.py              # FastAPI application with dependency injection
├── config.py            # Pydantic settings configuration
├── dependencies.py      # FastAPI security dependencies (APIKeyHeader, etc.)
├── middleware.py        # Utility functions for error responses
├── models/              # Pydantic data models
│   ├── __init__.py
│   ├── crawling.py      # Web crawling request/response models
│   └── geocoding.py     # Geocoding request/response models
├── services/            # Business logic services
│   ├── __init__.py
│   ├── crawling.py      # Crawl4AI integration service
│   ├── crawl_cache.py   # Crawling cache with TTL and deduplication
│   ├── geocoding.py     # Nominatim geocoding service
│   ├── cache.py         # Geocoding cache service
│   └── rate_limiter.py  # Rate limiting service
├── routers/             # FastAPI routers
│   ├── __init__.py
│   ├── crawling.py      # Web crawling API endpoints
│   └── geocoding.py     # Geocoding API endpoints
├── tests/               # Comprehensive test suite (160 tests)
│   ├── __init__.py
│   ├── conftest.py      # Test fixtures and configuration
│   ├── test_unit.py     # Unit tests for authentication dependencies
│   ├── test_integration.py  # Integration tests with FastAPI security
│   ├── test_cache.py    # Geocoding cache tests
│   ├── test_crawl_cache.py  # Crawling cache tests with screenshot keys
│   ├── test_crawling_service.py  # Crawling service and screenshot tests
│   ├── test_geocoding_service.py  # Geocoding service tests
│   └── test_rate_limiter.py  # Rate limiting tests
├── utils/              # Utility modules
│   ├── __init__.py
│   └── logging.py      # Advanced logging utilities with JSON formatting
├── ai_info/            # AI assistant documentation
│   └── docs/           # Reference documentation
│       ├── fastapi.md  # FastAPI code examples and patterns
│       ├── pydantic.md # Pydantic v2 examples and migration guide
│       ├── crawl4ai.md # Crawl4AI integration documentation
│       └── nominatim.md # Nominatim geocoding API reference
├── PRPs/               # Project Requirements and Plans
│   └── crawl4ai-endpoint.md  # Complete crawling implementation plan
├── logs/               # Log files (excluded from git)
│   └── .gitkeep        # Keep directory in git
├── .env                # Environment variables (not in git)
├── .env.example        # Example environment variables
├── pyproject.toml      # Project metadata, dependencies, and Ruff configuration
├── uv.lock            # UV dependency lock file
├── pytest.ini         # Pytest configuration
├── Makefile           # Common development commands
├── Claude.md          # AI assistant project documentation
├── .gitignore         # Git ignore file
└── README.md          # This file
```

## Development

### Adding New Endpoints

With FastAPI dependency injection, endpoints are explicit about their security requirements:

#### Protected Endpoints (Require Authentication)
```python
from dependencies import RequiredAuth

@app.get("/my-protected-endpoint")
async def my_protected_endpoint(_api_key: str = RequiredAuth):
    return {"message": "This endpoint requires authentication"}
```

#### Public Endpoints (No Authentication)
```python
@app.get("/my-public-endpoint")
async def my_public_endpoint():
    return {"message": "This endpoint is public"}
```

#### Optional Authentication
```python
from dependencies import OptionalAuth

@app.get("/my-optional-auth-endpoint")
async def my_optional_auth_endpoint(api_key: Optional[str] = OptionalAuth):
    if api_key:
        return {"message": "Authenticated user", "authenticated": True}
    return {"message": "Public access", "authenticated": False}
```

This approach makes security requirements explicit and visible in the code, improving maintainability and reducing security mistakes.

### CORS Configuration

CORS is currently configured to allow all origins (`*`). For production, update the CORS settings in `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],              # Specific methods
    allow_headers=["*"],
)
```

## Operational Features

### Advanced Logging System

The application features a comprehensive logging system with multiple output formats and rotation:

#### Console Logging
- Human-readable format for development
- Real-time log output with timestamps
- Configurable log levels

#### File Logging with Rotation
- Automatic log rotation when files exceed 10MB (configurable)
- Keeps 5 backup files by default (configurable)
- JSON format for structured data analysis
- Azure Blob Storage compatible format

#### Structured Logging Examples

**Console Output:**
```
2025-01-06 10:30:00 - middleware - INFO - Authentication attempt
```

**JSON File Output:**
```json
{
  "timestamp": "2025-01-06T10:30:00.123456Z",
  "level": "INFO",
  "logger": "middleware",
  "message": "Authentication attempt",
  "module": "middleware",
  "function": "dispatch",
  "line": 64,
  "path": "/protected",
  "method": "GET",
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "has_api_key": true,
  "client_ip": "192.168.1.100"
}
```

#### Security Features
- Automatic sanitization of sensitive data (API keys, passwords, tokens)
- Request correlation with unique IDs
- Authentication event tracking

#### Future Azure Blob Integration

The logging system is designed for future Azure Blob Storage integration:
- JSON format compatible with Azure Log Analytics
- Batch upload capabilities (planned)
- Managed Identity authentication support (planned)
- Automatic log archival to cloud storage (planned)

### Request Tracking

All authentication failures include unique request IDs for debugging and incident correlation. Use these IDs to trace issues across logs and error responses.

### Configuration Management

Environment variables are validated at startup with clear error messages:
- API key length requirements
- Valid log level formats
- Type validation for all settings

## API Documentation

### Environment-Based Documentation Visibility

The API documentation endpoints are automatically controlled by the `ENV` environment variable:

#### Development & Staging (ENV=development or ENV=staging)
When running in development or staging environments, full documentation is available:
- **Interactive API documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative API documentation (ReDoc)**: http://localhost:8000/redoc  
- **OpenAPI schema**: http://localhost:8000/openapi.json

#### Production (ENV=production)
In production environments, documentation endpoints are automatically hidden for security:
- All documentation URLs return **404 Not Found**
- No API schema information is exposed
- Reduces attack surface and prevents information disclosure

#### Configuration Examples
```bash
# Development/Testing - docs available
ENV=development

# Staging - docs available  
ENV=staging

# Production - docs hidden
ENV=production
```

**Default Behavior**: If `ENV` is not set, it defaults to `development` with docs enabled.

## Security Features

### Built-in Security Testing

The application includes comprehensive security testing against:
- **SQL Injection**: Malicious SQL in API keys
- **XSS Attacks**: Script injection attempts
- **Header Injection**: CRLF injection in headers
- **Unicode Attacks**: Normalization bypass attempts
- **Null Byte Injection**: String termination attacks
- **Extreme Input**: 10KB+ API key handling
- **Malformed Data**: Empty and whitespace-only inputs

### Security by Design

- **Default Deny**: All endpoints protected unless explicitly whitelisted
- **Case-Insensitive Headers**: HTTP standard compliant
- **Input Validation**: Comprehensive API key validation
- **Audit Logging**: All authentication attempts logged
- **Error Handling**: No information leakage in responses

## Production Deployment

### Security Checklist

1. **API Key Management**:
   - Use strong API keys (minimum 8 characters, recommend 32+)
   - Never commit `.env` files to version control
   - Implement key rotation procedures

2. **Network Security**:
   - Always use HTTPS in production
   - Implement rate limiting at gateway/proxy level
   - Restrict CORS origins to specific domains

3. **Monitoring**:
   - Monitor authentication failure patterns
   - Set up alerts for unusual request patterns
   - Use request IDs for incident correlation

4. **Configuration**:
   - Set `DEBUG=false` in production
   - Configure appropriate `LOG_LEVEL` (INFO or WARNING)
   - Validate all environment variables at startup

## Development & Contributing

### Development Workflow

1. Create a feature branch
2. Make your changes
3. Run the complete quality workflow:
   ```bash
   make quality  # Runs: ruff format, ruff check --fix, pytest
   ```
4. Ensure all 160 tests pass and zero linting issues
5. Submit a pull request

### Code Quality Standards

- **Test Coverage**: All new features must include tests
- **Security Testing**: Add security tests for new attack vectors
- **Linting**: Zero Ruff violations required
- **Type Safety**: Full type hint coverage
- **Documentation**: Update README for new features

### Adding Security Tests

When adding new security tests, follow the pattern in `TestSecurityTesting`:
```python
def test_new_attack_vector(self, client: TestClient):
    """Test protection against new attack type."""
    malicious_headers = {"X-API-KEY": "malicious-payload"}
    response = client.get("/protected", headers=malicious_headers)
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Invalid API key"
    assert "request_id" in data
```

## License

This project is proprietary software developed for internal company use only. All rights reserved. Distribution, modification, or sharing outside the company is strictly prohibited.
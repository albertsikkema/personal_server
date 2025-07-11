# FastAPI Application with Security by Design

An enterprise-grade FastAPI application implementing JWT Bearer token authentication using FastAPI-Users. Features user management, automatic OpenAPI security documentation, production-ready operational capabilities, comprehensive security testing, and enhanced observability.

**Repository**: [https://github.com/epblc/fastapi_template](https://github.com/epblc/fastapi_template)

## Features

### 🔒 Security
- **FastAPI-Users Integration**: Modern user management with JWT Bearer token authentication
- **User Registration & Login**: Complete user lifecycle with secure registration and JWT login endpoints
- **JWT Bearer Authentication**: Secure authentication using Bearer tokens with automatic validation
- **OpenAPI Security Documentation**: Automatic Bearer token security scheme documentation in Swagger/ReDoc
- **Comprehensive Security Testing**: Protection against injection attacks, XSS, and malformed input
- **Standards-Compliant**: HTTP Authorization header with Bearer token standard

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

### 🤖 MCP Integration with JWT Bearer Authentication
- **Model Context Protocol**: Expose APIs as MCP tools for LLM clients with JWT Bearer token authentication
- **FastMCP Server**: Integrated MCP server mounted at `/mcp-server/mcp` endpoint
- **Geocoding Tool**: Convert city names to coordinates via MCP
- **Streamable HTTP Transport**: Modern MCP transport protocol with per-request JWT authentication
- **Service Reuse**: Identical functionality to REST API endpoints with same authentication

**Authentication Behavior**: JWT Bearer tokens are validated on every MCP request using the same FastAPI-Users authentication system. The FastMCP client automatically includes the Bearer token in each request, providing secure per-request authentication following industry-standard JWT patterns.

## FastAPI Security Benefits

This application leverages **FastAPI's official security implementation** for maximum compatibility and maintainability:

### 🎯 **Standards Compliance**
- Uses `fastapi.security.HTTPBearer` for JWT Bearer token authentication
- Integrates FastAPI-Users for modern authentication patterns
- Follows OpenAPI 3.0 Bearer authentication standards
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
async def protected_endpoint(user: User = Depends(current_active_user)):
    return {"message": f"Authenticated as {user.email}"}
```

## Security Model

This application uses **FastAPI-Users** with JWT Bearer token authentication:
- User management handled through FastAPI-Users with user registration and login
- Authentication is handled through FastAPI dependencies using `Depends(current_active_user)`
- Protected endpoints explicitly declare authentication requirements
- Public endpoints require no authentication dependencies
- Currently public endpoints:
  - `/` - Root endpoint
  - `/health` - Health check
  - `/auth/register` - User registration
  - `/auth/jwt/login` - JWT login
  - `/docs` - Swagger UI documentation (includes Bearer token authentication UI)
  - `/redoc` - ReDoc documentation (includes security information)
  - `/openapi.json` - OpenAPI schema (includes Bearer token security definitions)

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
# Edit .env and set your JWT_SECRET
```

## Configuration

Create a `.env` file in the project root with the following:

```env
# Required: JWT secret for token authentication (minimum 32 characters)
JWT_SECRET=your-super-secret-jwt-signing-key-here-minimum-32-characters

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
- **JWT_SECRET**: Required, minimum 32 characters for JWT token signing security
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

#### Protected Endpoints (JWT Bearer Token Required)

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
  -H "Authorization: Bearer <your-access-token>" \
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
  -H "Authorization: Bearer <your-access-token>" \
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
  -H "Authorization: Bearer <your-access-token>" \
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
  -H "Authorization: Bearer <your-access-token>" \
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
  -H "Authorization: Bearer <your-access-token>"
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
- `401`: JWT Bearer token required, invalid, or expired
- `422`: Invalid input parameters (URL format, dimension limits, etc.)
- `429`: Rate limit exceeded
- `503`: Crawl4AI service unavailable
- `504`: Crawl4AI service timeout

## 🔍 Geocoding API

Convert city names to geographic coordinates using the Nominatim service.

### Usage Example

```bash
curl -X GET "http://localhost:8000/geocode/city?city=London" \
  -H "Authorization: Bearer <your-access-token>"
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

This application uses FastAPI-Users for comprehensive user management with JWT Bearer token authentication.

#### User Registration and Login Flow

1. **Register a new user**:
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secure-password",
    "is_active": true,
    "is_superuser": false,
    "is_verified": false
  }'
```

2. **Login to get access token**:
```bash
curl -X POST "http://localhost:8000/auth/jwt/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=secure-password"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

3. **Use Bearer token in API requests**:
```bash
curl -H "Authorization: Bearer <your-access-token>" http://localhost:8000/protected
```

#### Using Swagger UI

1. Open http://localhost:8000/docs in your browser
2. Register a new user using the `/auth/register` endpoint
3. Login using the `/auth/jwt/login` endpoint to get your access token
4. Click the "Authorize" button in the top right
5. Enter your access token in the "HTTPBearer (Authorization)" field with "Bearer " prefix
6. Click "Authorize" to authenticate
7. Now you can test protected endpoints directly in the UI

#### OpenAPI Security Schema

The application automatically generates OpenAPI security documentation:
```json
{
  "components": {
    "securitySchemes": {
      "HTTPBearer": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "JWT Bearer token authentication"
      }
    }
  }
}
```

### Error Responses

Authentication failures return enhanced error responses with request tracking:
```json
{
  "detail": "Not authenticated",
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

With FastAPI-Users dependency injection, endpoints are explicit about their security requirements:

#### Protected Endpoints (Require Authentication)
```python
from fastapi_users import current_active_user
from models.user import User

@app.get("/my-protected-endpoint")
async def my_protected_endpoint(user: User = Depends(current_active_user)):
    return {"message": f"This endpoint requires authentication. Hello {user.email}!"}
```

#### Public Endpoints (No Authentication)
```python
@app.get("/my-public-endpoint")
async def my_public_endpoint():
    return {"message": "This endpoint is public"}
```

#### Optional Authentication
```python
from fastapi_users import current_user
from models.user import User
from typing import Optional

@app.get("/my-optional-auth-endpoint")
async def my_optional_auth_endpoint(user: Optional[User] = Depends(current_user)):
    if user:
        return {"message": f"Authenticated user: {user.email}", "authenticated": True}
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
- **SQL Injection**: Malicious SQL in JWT tokens and user input
- **XSS Attacks**: Script injection attempts
- **Header Injection**: CRLF injection in headers
- **Unicode Attacks**: Normalization bypass attempts
- **Null Byte Injection**: String termination attacks
- **JWT Token Attacks**: Invalid tokens, expired tokens, malformed tokens
- **Authentication Bypass**: Attempts to access protected endpoints without tokens
- **Malformed Data**: Empty and whitespace-only inputs

### Security by Design

- **Default Deny**: All endpoints protected unless explicitly whitelisted
- **JWT Standards**: HTTP Bearer token authentication following RFC 6750
- **Input Validation**: Comprehensive JWT token validation and user input sanitization
- **Audit Logging**: All authentication attempts and user actions logged
- **Error Handling**: No information leakage in responses
- **User Management**: Secure user registration, login, and session management

## Production Deployment

### Security Checklist

1. **JWT Secret Management**:
   - Use strong JWT secrets (minimum 32 characters, recommend 64+)
   - Never commit `.env` files to version control
   - Implement JWT secret rotation procedures
   - Consider using HSA256 algorithm for JWT signing

2. **User Management**:
   - Implement proper user registration validation
   - Use secure password policies
   - Consider email verification for new users
   - Implement user account lockout policies

3. **Token Security**:
   - Set appropriate JWT expiration times
   - Implement token refresh mechanisms if needed
   - Store tokens securely on client side
   - Consider token revocation strategies

4. **Network Security**:
   - Always use HTTPS in production
   - Implement rate limiting at gateway/proxy level
   - Restrict CORS origins to specific domains

5. **Monitoring**:
   - Monitor authentication failure patterns
   - Set up alerts for unusual login patterns
   - Use request IDs for incident correlation
   - Track failed login attempts per user

6. **Configuration**:
   - Set `DEBUG=false` in production
   - Configure appropriate `LOG_LEVEL` (INFO or WARNING)
   - Validate all environment variables at startup
   - Ensure JWT_SECRET is properly configured

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
    malicious_headers = {"Authorization": "Bearer malicious-payload"}
    response = client.get("/protected", headers=malicious_headers)
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Not authenticated"
    assert "request_id" in data
```

## 🚀 CI/CD Pipeline

This project includes a **production-ready CI/CD pipeline** using GitHub Actions that ensures code quality, security, and reliability on every commit and pull request. The pipeline has successfully **detected and remediated 17 real security vulnerabilities** and uses official security actions for enterprise-grade protection.

### Pipeline Overview

The CI/CD system consists of two main workflows providing comprehensive quality assurance and security protection:

1. **Quality & Testing**: Parallel execution of code quality checks and build verification
2. **Security**: Official security scanning with real vulnerability detection and remediation

### Quality Workflow

The quality workflow (`.github/workflows/quality.yml`) runs on every push and pull request to `main` and `dev` branches:

#### Features
- **Smart Path Filtering**: Only runs when relevant files change (Python, config, workflows)
- **Parallel Execution**: Quality checks and build verification run concurrently (30% performance improvement)
- **Python 3.13**: Uses the latest stable Python version for testing
- **Fast Dependency Management**: Uses uv for 10-100x faster dependency resolution
- **Branch-Specific Caching**: Optimized cache performance across development branches
- **CI-Safe Quality Checks**: Uses `make check-commit` (no auto-fixes in CI)
- **Enhanced Build Testing**: Detailed application startup validation with comprehensive error reporting

#### Workflow Jobs

1. **Change Detection**: Determines if Python code or documentation changed
2. **Code Quality**: Runs linting, formatting checks, and tests on Python 3.13 (parallel)
3. **Build Check**: Validates application startup and health endpoint (parallel)

#### Example Run
```yaml
✅ Code Quality (Python 3.13)
├── Install uv and dependencies
├── Run make check-commit
├── Upload coverage reports
└── Complete in ~2 minutes


✅ Build Check
├── Validate application imports
├── Test server startup
└── Complete in ~1 minute
```

### Security Workflow

The security workflow (`.github/workflows/security.yml`) performs comprehensive security analysis using **official security actions**:

#### Real Security Success
- **17 Vulnerabilities Detected**: Successfully identified real security issues across critical packages
- **All Vulnerabilities Fixed**: Strategic dependency updates resolved all security issues
- **Production-Ready**: Security workflow now passes with zero vulnerabilities

#### Features
- **Official PyPA pip-audit Action**: Official dependency vulnerability scanning with environment consistency
- **Official PyCQA Bandit Action**: Source code security analysis with GitHub Security tab integration
- **Parallel Security Jobs**: pip-audit and bandit run simultaneously for maximum efficiency
- **Scheduled Scanning**: Weekly security scans on Monday for ongoing protection
- **Severity Filtering**: Bandit configured for medium/high severity issues only

#### Security Tools

1. **PyPA pip-audit**: Official Python package vulnerability scanner with local environment scanning
2. **PyCQA Bandit**: Official Python source code security analysis with SARIF reporting
3. **GitHub Security Tab**: Native integration for centralized vulnerability management

#### Workflow Jobs

1. **Dependency Vulnerability Scan**: Official PyPA pip-audit scanning uv-managed environment (parallel)
2. **Code Security Scan**: Official PyCQA bandit analysis with severity filtering (parallel)

### Automated Dependency Management

The project includes Dependabot configuration (`.github/dependabot.yml`) for automated dependency updates:

- **Weekly Updates**: Automatically checks for dependency updates
- **Managed PRs**: Limits to 10 open PRs at a time
- **Conventional Commits**: Uses proper commit message format

### Performance & Optimization

#### Build Performance
- **uv Caching**: 10-100x faster dependency resolution vs pip
- **Parallel Job Architecture**: Quality and build checks run concurrently (30% time reduction)
- **Branch-Specific Caching**: Optimized cache performance across development branches
- **Path-Based Filtering**: Only runs workflows when relevant files change
- **Official Actions**: No custom dependency installation or complex scripting

#### Typical Build Times
- **Quality Workflow**: ~5 minutes (parallel: quality checks + build verification)
- **Security Workflow**: ~3 minutes (parallel: dependency + source code scanning)  
- **Total Pipeline**: ~5 minutes (down from ~7 minutes with parallel optimization)
- **Cache Hit**: ~2 minutes (when dependencies unchanged)

### Local Development Integration

The CI/CD pipeline uses the same commands available locally:

```bash
# Same command used in CI quality workflow
make check-commit

# Test the complete quality workflow locally (what CI runs)
make quality

# Run security scanning locally
uv run pip-audit --desc
uv run bandit -r . --format=text
```

### Status Checks & Branch Protection

The following status checks are recommended for branch protection:

- `Quality & Testing / Code Quality`
- `Quality & Testing / Build Check`
- `Security / Dependency Vulnerability Scan`
- `Security / Code Security Scan`

### Artifacts & Reports

The workflows generate several artifacts for debugging and monitoring:

#### Quality Artifacts
- **Coverage Reports**: HTML coverage reports (30-day retention)
- **Test Results**: Detailed test output and timing

#### Security Artifacts
- **GitHub Security Tab**: SARIF reports from bandit automatically uploaded
- **Security Summaries**: Comprehensive workflow summaries with tool information
- **Vulnerability Detection**: Real-time security issue identification and remediation guidance

### Monitoring & Alerts

The CI/CD system provides comprehensive monitoring:

#### GitHub Integration
- **Status Checks**: Pass/fail status on PRs and commits
- **Notifications**: Email alerts for workflow failures
- **Dashboard**: GitHub Actions dashboard for workflow monitoring

#### Coverage Tracking
- **Codecov Integration**: Automatic coverage reporting
- **Coverage Trends**: Track coverage changes over time
- **PR Coverage**: Coverage diff on pull requests

### Configuration Files

The CI/CD system uses these configuration files:

- `.github/workflows/quality.yml`: Main quality and testing workflow
- `.github/workflows/security.yml`: Security scanning workflow
- `.github/dependabot.yml`: Dependency update configuration
- `Makefile`: Commands used by both local development and CI

### Troubleshooting

#### Common Issues

1. **Linting Failures**: Run `make fix` locally to auto-fix issues
2. **Test Failures**: Run `make test` locally to reproduce issues
3. **Security Scan Failures**: Review security reports in workflow artifacts
4. **Build Timeouts**: Check for dependency resolution issues

#### Debug Commands

```bash
# Validate workflow YAML syntax
uv run python -c "import yaml; yaml.safe_load(open('.github/workflows/quality.yml'))"

# Test make targets locally
make check-commit
make security

# Check workflow file paths
find .github -name "*.yml" -o -name "*.yaml"
```

### Best Practices

#### For Developers
1. Always run `make quality` before pushing code
2. Keep PRs small to reduce CI/CD time
3. Add tests for new features to maintain coverage
4. Update documentation when adding new features

#### For Maintainers
1. Monitor workflow failure patterns
2. Update security scanning tools regularly
3. Review and merge Dependabot PRs promptly
4. Keep workflow files updated with latest actions

### Security Achievement Highlights

This CI/CD pipeline has demonstrated real-world security value:

#### **Vulnerability Discovery & Remediation**
- **17 vulnerabilities detected** across critical packages (cryptography, jinja2, requests, urllib3, twisted, etc.)
- **100% remediation success** through strategic dependency updates
- **Zero false positives** - all detected issues were legitimate security concerns
- **Production-ready security posture** achieved

#### **Security Tool Integration**
- **Official Actions**: PyPA pip-audit and PyCQA bandit (no custom implementations)
- **Environment Consistency**: pip-audit scans exact uv-managed environment
- **GitHub Security Integration**: Native SARIF reporting and Security tab visibility
- **Continuous Protection**: Weekly scheduled scans and real-time PR protection

### Future Enhancements

The CI/CD pipeline is designed for extensibility:

- **Deployment Automation**: Ready for automatic deployment workflows
- **Release Automation**: Semantic versioning and automated releases
- **Performance Testing**: Load testing integration
- **Multi-Environment**: Support for staging and production environments
- **Advanced Security**: Slack notifications for critical findings, workflow duration monitoring

## License

This project is proprietary software developed for internal company use only. All rights reserved. Distribution, modification, or sharing outside the company is strictly prohibited.
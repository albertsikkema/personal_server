# Claude.md - Project Documentation Reference

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Core Principles

KISS (Keep It Simple, Stupid): Simplicity should be a key goal in design. Choose straightforward solutions over complex ones whenever possible. Simple solutions are easier to understand, maintain, and debug.

YAGNI (You Aren't Gonna Need It): Avoid building functionality on speculation. Implement features only when they are needed, not when you anticipate they might be useful in the future.

Dependency Inversion: High-level modules should not depend on low-level modules. Both should depend on abstractions. This principle enables flexibility and testability.

Open/Closed Principle: Software entities should be open for extension but closed for modification. Design your systems so that new functionality can be added with minimal changes to existing code.

## 🤖 AI Assistant Guidelines

### Context Awareness

- When implementing features, always check existing patterns first
- Prefer composition over inheritance in all designs
- Use existing utilities before creating new ones
- Check for similar functionality in other domains/features

### Common Pitfalls to Avoid

- Creating duplicate functionality
- Overwriting existing tests
- Modifying core frameworks without explicit instruction
- Adding dependencies without checking existing alternatives

### Workflow Patterns

- Preferably create tests BEFORE implementation (TDD, Test Driven Development)
- Use "think hard" for architecture decisions
- Break complex tasks into smaller, testable units
- Validate understanding before implementation

## 🧱 Code Structure & Modularity

- **Never create a file longer than 500 lines of code.** If a file approaches this limit, refactor by splitting it into modules or helper files.
- **Functions should be short and focused sub 50 lines of code** and have a single responsibility.
- **Classes should be short and focused sub 50 lines of code** and have a single responsibility.
- **Organize code into clearly separated modules**, grouped by feature or responsibility.

## Architecture

Strict vertical slice architecture with tests that live next to the code they test.

```
src/project/
    __init__.py
    main.py
    tests/test_main.py
    conftest.py
    module_one/  (eg. database, core, auth)
        __init__.py
        module_one.py
        tests/
            test_module_one.py
    module_two/  (eg. api, ui, cli)
        __init__.py
        module_two.py
        tests/
            test_module_two.py
    
    features/  (eg. business logic, tools, etc.)
        feature_one/
            __init__.py
            feature.py
            tests/
                test_feature.py
```

Features can also be part of modules if the module for example is a api integration or a cli tool.

eg
```
src/project/
    module_one/  (api integration with crm service)
        __init__.py
        module_one.py
        tests/
            test_module_one.py
        features/
            feature_one/  (CRM service integration slice)
                __init__.py
                feature.py
                tests/
                    test_feature.py
```

## Documentation Reference

Documentation can be found in /ai_info/docs. 

### FastAPI Documentation
**File:** `ai_info/docs/fasttapi.md`  
**Description:** Comprehensive FastAPI code snippets and examples  
**Key Topics:**
- Installation and setup (pip install "fastapi[standard]", virtual environments)
- Basic application structure (creating FastAPI app, defining endpoints)
- HTTP methods (GET, POST, PUT, DELETE decorators)
- Request handling (path parameters, query parameters, request bodies)
- Pydantic models integration for data validation
- Type hints and automatic validation
- Dependency injection system
- Authentication (OAuth2, security schemes)
- Middleware (CORS, TrustedHost)
- Advanced features (sub-applications, APIRouter, WebSocket)
- Testing with TestClient
- Deployment (Uvicorn, Gunicorn, Docker)
- Database integration examples
- Settings and configuration management
- Async/await patterns

### Pydantic Documentation
**File:** `ai_info/docs/pydantic.md`  
**Description:** Comprehensive Pydantic v2 code snippets and examples  
**Key Topics:**
- Installation (pip, uv, conda)
- BaseModel definition and usage
- Data validation and type coercion
- Field constraints and metadata
- Model serialization (model_dump, model_dump_json)
- Model validation methods (model_validate, model_validate_json)
- Custom validators (field_validator, model_validator, BeforeValidator)
- Generic models and type variables
- Nested models and complex data structures
- Performance optimization (TypeAdapter, tagged unions)
- JSON schema generation
- Migration from Pydantic v1 to v2
- Error handling and ValidationError
- Advanced features (RootModel, computed fields)
- Integration with external services (Redis, HTTP APIs)


## Project Dependencies

### Core Dependencies
- **FastAPI**: Modern web framework for building APIs with Python 3.9+ based on standard Python type hints
- **Pydantic**: Data validation and settings management using Python type annotations
- **Uvicorn**: Lightning-fast ASGI server implementation, using uvloop and httptools

### Optional Dependencies (from fastapi[standard])
- **python-multipart**: Required for form data parsing
- **httpx**: Modern HTTP client for testing and external API calls
- **jinja2**: Templating engine for HTML responses
- **python-jose**: For JWT token handling in authentication

## Common Usage Patterns

### FastAPI Quick Start
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    tax: float | None = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/items/")
async def create_item(item: Item):
    return item
```

### Running the Application
```bash
# Development
$ fastapi dev main.py

# Production
$ fastapi run main.py --port 80
```

## Project-Specific Implementation

### Authentication System

This project implements **FastAPI's official security system** using dependency injection:

#### Core Security Components
```python
# dependencies.py
from fastapi.security import APIKeyHeader
from fastapi import Security, Depends

api_key_header = APIKeyHeader(
    name="X-API-KEY", 
    auto_error=False,
    description="API key for authentication"
)

async def verify_api_key(api_key: Annotated[str, Security(api_key_header)]) -> str:
    # Authentication logic with custom error responses
    
RequiredAuth = Depends(verify_api_key)  # Helper alias
OptionalAuth = Depends(optional_api_key)  # Optional auth
```

#### Usage in Endpoints
```python
# Protected endpoint - requires authentication
@app.get("/protected")
async def protected_endpoint(_api_key: str = RequiredAuth):
    return {"message": "Authenticated"}

# Public endpoint - no authentication
@app.get("/public")
async def public_endpoint():
    return {"message": "Public"}

# Optional authentication
@app.get("/optional")
async def optional_endpoint(api_key: Optional[str] = OptionalAuth):
    return {"authenticated": bool(api_key)}
```

#### Error Response Format
```python
# Custom exception for consistent error responses
class AuthHTTPException(HTTPException):
    def __init__(self, status_code: int, message: str):
        self.response_content = {
            "detail": message,
            "request_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        super().__init__(status_code=status_code, detail=self.response_content)
```

#### OpenAPI Integration
- Automatic security scheme documentation
- Swagger UI "Authorize" button 
- Security requirements per endpoint
- Type-safe authentication

## 📍 Geocoding API

The application now includes a comprehensive geocoding API that converts city names to geographic coordinates using the Nominatim service.

### Features
- **Rate Limiting**: Complies with Nominatim's 1 request/second policy
- **Caching**: 24-hour TTL to minimize API calls
- **User Rate Limiting**: 10 requests/minute per IP
- **Authentication**: Requires API key for all endpoints
- **Error Handling**: Comprehensive error responses with proper status codes

### Endpoints

#### Geocode City
```
GET /geocode/city?city={city_name}
```

**Parameters:**
- `city` (string, required): City name to geocode (1-200 characters)

**Response Example:**
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

#### Health Check
```
GET /geocode/health
```

**Response Example:**
```json
{
  "service": "geocoding",
  "status": "healthy",
  "cache_size": 42,
  "cache_ttl_hours": 24,
  "rate_limiter_active": true,
  "user_agent": "FastAPI Application/1.0"
}
```

#### Clear Cache (Admin)
```
POST /geocode/cache/clear
```

### Configuration

Add to `.env` or environment variables:
```bash
GEOCODING_CACHE_TTL_HOURS=24
GEOCODING_USER_RATE_LIMIT=10/minute
```

### Dependencies
- `httpx`: HTTP client for Nominatim API calls
- `slowapi`: Rate limiting middleware

### Architecture

The geocoding feature follows the established vertical slice architecture:

```
geocoding/
├── models/geocoding.py          # Pydantic models
├── services/
│   ├── rate_limiter.py         # Nominatim rate limiting (1 req/sec)
│   ├── cache.py                # In-memory caching (24h TTL)
│   └── geocoding.py            # Main geocoding service
├── routers/geocoding.py        # API endpoints
└── tests/
    ├── test_rate_limiter.py    # Rate limiter unit tests
    ├── test_cache.py           # Cache unit tests
    ├── test_geocoding_service.py # Service unit tests
    └── test_integration.py     # Integration tests (in main tests/)
```

### Nominatim Compliance

The implementation strictly follows Nominatim's usage policy:
- Maximum 1 request per second (enforced by RateLimiter)
- User-Agent header provided with all requests
- Results cached to minimize API calls
- Proper attribution (handled in client implementation)

## Testing

**Always create Pytest unit tests for new features** (functions, classes, routes, etc)
Tests are always created in the same directory as the code they test in a tests/ directory. Create the tests directory if it doesn't exist.

**After updating any logic**, check whether existing unit tests need to be updated. If so, do it following the implementation.

Always test individual functions and classes.

### Testing Approach

#### Unit Tests (9 tests)
- Authentication dependency validation
- Custom exception handling
- Error response format verification

#### Integration Tests (31 tests)  
- Full API endpoint testing
- Security attack simulations
- OpenAPI documentation verification
- Environment-based behavior testing

#### Running Tests
```bash
# All tests
make test

# With coverage
pytest --cov=.

# Quality workflow (lint + test)
make quality
```

## Best Practices

1. **Type Hints**: Always use type hints for automatic validation and documentation
2. **Pydantic Models**: Define request/response schemas using Pydantic BaseModel
3. **Dependency Injection**: Use FastAPI's dependency system for shared logic and authentication
4. **Async/Await**: Use async functions for I/O-bound operations
5. **Error Handling**: Utilize HTTPException and proper status codes with request tracking
6. **Security**: Use FastAPI Security classes (`APIKeyHeader`, `Security()`, `Depends()`)
7. **Testing**: Use TestClient for comprehensive API testing with dependency mocking
8. **Documentation**: FastAPI automatically generates OpenAPI documentation with security schemas

For more best practices, see /ai_info/fastapi-best-practices.md

## Project Structure

```
fastapi_template/
├── main.py              # FastAPI application with dependency injection
├── config.py            # Pydantic settings configuration
├── dependencies.py      # FastAPI security dependencies (APIKeyHeader, etc.)
├── middleware.py        # Utility functions for error responses
├── tests/               # Test suite
│   ├── conftest.py      # Test fixtures  
│   ├── test_unit.py     # Unit tests for authentication dependencies
│   └── test_integration.py  # Integration tests with FastAPI security
├── utils/               # Utility modules
│   └── logging.py       # Advanced logging utilities
├── .env                 # Environment variables (not in git)
├── requirements.txt     # Python dependencies
├── Makefile            # Common development commands
└── Claude.md           # This documentation file
```

## Common Commands

### Development Workflow
```bash
# Start development server
make run

# Run complete quality workflow (lint + format + test)
make quality

# Run tests only
make test

# Run with coverage
make test-cov

# Lint and format code
make fix

# See all available commands
make help
```

### Key Environment Variables
```bash
# Required
API_KEY=your-secret-api-key-here    # Minimum 8 characters

# Optional
ENV=development                     # Controls docs visibility
DEBUG=true                         # Debug mode
LOG_LEVEL=INFO                     # Logging level
```

## Configuration Notes

- Virtual environment setup is recommended before installation
- Upgrade pip before installing dependencies: `python -m pip install --upgrade pip`
- For production deployment, use Gunicorn with Uvicorn workers
- Environment variables can be managed using Pydantic Settings
- Tests ensure all 40 test cases pass before deployment
- Use `make quality` before committing code changes

## 📎 Style & Conventions

- **Use Python** as the primary language.
- **Follow PEP8**, always use type hints, and format with `ruff`.
- **Use `pydanticv2` for data validation**.
- **ALWAYS use classes, data types, data models, for typesafety and verifiability**
- **ALWAYS use docstrings for every function** using the Google style:

  ```python
  def example():
      """
      Brief summary.

      Args:
          param1 (type): Description.

      Returns:
          type: Description.

      Raises:
          Exception: Description.
      """
  ```

## 🛠️ Environment Setup

```bash
# Create and activate virtual environment with uv
uv venv
source .venv/bin/activate  # On Unix/macOS
# .venv\Scripts\activate  # On Windows

# Install dependencies
uv sync

# Install package in development mode
uv pip install -e .
```

## 🛠️ Development Commands

```bash
# Run all tests
uv run pytest

# Run specific tests
uv run pytest concept_library/full_review_loop/tests/ -v

# Format code
uv run ruff format .

# Run linter
uv run ruff check .

# Run type checker
uv run mypy .
```

## 🛠️ UV Package Management

This project uses UV for Python package management. Key commands include:

```bash
# Create virtual environment
uv venv

# Install dependencies from pyproject.toml
uv sync

# Install a specific package
uv add requests

# Remove a package
uv remove requests

# Run a Python script or command
uv run python script.py
uv run pytest

# Install editable packages
uv pip install -e .
```

When running scripts or tools, always use `uv run` to ensure proper virtual environment activation:

```bash
# Preferred way to run commands
uv run pytest
uv run black .

# Running tools without installing
uvx black .
uvx ruff check .
```

## 🛠️ BRANCHING STRATEGY

This repository follows a develop → main branching strategy, where:

- `main` is the production branch containing stable releases
- `dev` is the integration branch where features are merged
- Feature branches are created from `dev` for work in progress

When creating branches, follow these naming conventions:

- Feature branches: `feature/descriptive-name`
- Bug fix branches: `fix/issue-description`
- Documentation branches: `docs/what-is-changing`
- Refactoring branches: `refactor/what-is-changing`

## Behavioural Guidelines

- Always use `uv` for package management.
- Always use `ruff` for linting.

- **NEVER ASSUME OR GUESS**
- When in doubt, ask for clarification or ask for help. More often than not you can do websearch to find relevant examples or check ai_info/docs/ for examples that the user have added.

- **Always confirm file paths & module names** exist before using them.

- **Comment non-obvious code** and ensure everything is understandable to a mid-level developer.
- When writing complex logic, **add an inline `# Reason:` comment** explaining the why, not just the what.

- **KEEP README.md UPDATED**
- Whenever you make changes to the codebase, update the README.md file to reflect the changes. Especially if you add configuration changes or new features.

- **ALWAYS keep CLAUDE.md UPDATED**
- Add new dependencies to CLAUDE.md
- Add important types and patterns to CLAUDE.md

## IMPORTANT TYPES & PATTERNS

### Geocoding API Models

```python
# Core geocoding models (models/geocoding.py)
from typing import Optional
from pydantic import BaseModel, Field

class Location(BaseModel):
    lat: float = Field(..., ge=-90.0, le=90.0)
    lon: float = Field(..., ge=-180.0, le=180.0)

class GeocodingResponse(BaseModel):
    city: str
    location: Location
    display_name: str
    place_id: Optional[int] = None
    boundingbox: Optional[list[float]] = None
    timestamp: str
    cached: bool = False
```

### Rate Limiting Pattern

```python
# services/rate_limiter.py
class RateLimiter:
    def __init__(self, max_requests: int = 1, time_window: float = 1.0):
        self.max_requests = max_requests
        self.time_window = time_window
        self.last_request_time: Optional[float] = None
        self._lock = asyncio.Lock()
    
    async def acquire(self):
        async with self._lock:
            current_time = time.time()
            if self.last_request_time is not None:
                time_since_last = current_time - self.last_request_time
                if time_since_last < self.time_window:
                    sleep_time = self.time_window - time_since_last
                    await asyncio.sleep(sleep_time)
            self.last_request_time = time.time()
```

### Caching Pattern

```python
# services/cache.py  
class GeocodingCache:
    def __init__(self, ttl_hours: int = 24):
        self._cache: dict[str, tuple[dict, datetime]] = {}
        self.ttl = timedelta(hours=ttl_hours)
    
    def _get_key(self, city: str) -> str:
        # Normalize: case-insensitive, whitespace-trimmed
        normalized = city.lower().strip()
        return hashlib.md5(normalized.encode()).hexdigest()
```

### Router Pattern with Rate Limiting

```python
# routers/geocoding.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(
    prefix="/geocode",
    tags=["geocoding"],
    dependencies=[RequiredAuth]  # Apply auth to all routes
)

@router.get("/city", response_model=GeocodingResponse)
@limiter.limit(settings.GEOCODING_USER_RATE_LIMIT)
async def geocode_city(
    request: Request,  # Required for rate limiter
    city: str = Query(..., min_length=1, max_length=200)
):
    # Implementation
```

### Service Pattern with HTTP Client

```python
# services/geocoding.py
class GeocodingService:
    def __init__(self):
        self.rate_limiter = RateLimiter(max_requests=1, time_window=1.0)
        self.cache = GeocodingCache(ttl_hours=settings.GEOCODING_CACHE_TTL_HOURS)
        self.user_agent = f"{settings.APP_NAME}/1.0"
        self.base_url = "https://nominatim.openstreetmap.org"
    
    async def geocode_city(self, city: str) -> Optional[GeocodingResponse]:
        # Check cache first
        cached = self.cache.get(city)
        if cached:
            response = GeocodingResponse(**cached)
            response.cached = True
            return response
        
        # Rate limit before API call
        await self.rate_limiter.acquire()
        
        # Make HTTP request with proper headers
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/search",
                params={"q": city, "format": "json"},
                headers={"User-Agent": self.user_agent},
                timeout=10.0
            )
            # Process response...
```

### Dependencies Added
- `slowapi==0.1.9`: Rate limiting middleware
- `httpx`: Already included, used for HTTP API calls
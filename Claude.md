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
- When writing titles and descriptions for comments and PRs, always follow the standards in ai_info/docs/conventional_commits.md

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

This project has been successfully migrated from pip to uv for Python package management. Key commands include:

```bash
# Create virtual environment and install dependencies
uv sync

# Install a specific package
uv add requests

# Remove a package
uv remove requests

# Run a Python script or command
uv run python script.py
uv run pytest

# Update all dependencies
uv sync --upgrade

# Install editable packages
uv pip install -e .
```

When running scripts or tools, always use `uv run` to ensure proper virtual environment activation:

```bash
# Preferred way to run commands
uv run pytest
uv run ruff check .
uv run fastapi dev main.py

# Running tools without installing
uvx black .
uvx ruff check .
```

### Migration Completed

✅ **Successfully migrated from pip to uv (2025-01-11)**

**Migration Summary:**
- **pyproject.toml**: Updated with all dependencies organized into main and dev groups
- **Makefile**: All pip commands replaced with uv equivalents
- **Dependencies**: 72 packages successfully resolved with no conflicts
- **Testing**: All 160 tests pass with uv run pytest
- **Linting**: All code quality checks pass with uv run ruff check
- **Performance**: 10-100x faster dependency resolution and installation
- **Cleanup**: Removed requirements.txt, fastapi_app.egg-info/, and old venv/ directory

**Key Benefits Achieved:**
1. **Faster dependency resolution**: UV resolves 72 packages in milliseconds vs. minutes with pip
2. **Unified project management**: Single tool for virtual environments, dependencies, and script execution
3. **Better reproducibility**: uv.lock ensures consistent environments across machines
4. **Improved developer experience**: Simplified commands and better error messages
5. **Modern Python packaging**: Following current best practices with pyproject.toml

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

## 📍 Web Crawling API

The application includes a comprehensive web crawling API that integrates with Crawl4AI to provide advanced crawling capabilities with screenshot capture and recursive link following.

### Features
- **Multi-URL Crawling**: Process up to 10 URLs per request with async processing
- **Screenshot Capture**: Full-page screenshots with custom dimensions and validation
- **Recursive Crawling**: Follow internal and external links with configurable depth
- **Smart URL Deduplication**: Normalize URLs to prevent duplicate crawling
- **Rate Limiting**: Service-level (1 req/sec) and user-level (10 req/min) protection
- **Caching**: TTL-based caching with O(1) invalidation performance
- **Authentication**: JWT token support for Crawl4AI service

### Core Architecture

The crawling feature follows the established vertical slice architecture:

```
crawling/
├── models/crawling.py          # Pydantic models with validation
├── services/
│   ├── crawling.py            # Main Crawl4AI integration service
│   ├── crawl_cache.py         # Caching with URL normalization
│   └── rate_limiter.py        # Rate limiting service
├── routers/crawling.py        # API endpoints with rate limiting
└── tests/
    ├── test_crawling_service.py # Service unit tests
    ├── test_crawl_cache.py     # Cache unit tests
    └── test_integration.py     # Integration tests
```

### Key Implementation Patterns

#### Async Task-Based API Integration

```python
# services/crawling.py
class CrawlingService:
    async def _crawl_single_url(self, url: str, request: CrawlRequest, depth: int = 0) -> CrawlResult:
        """Crawl using Crawl4AI async task pattern."""
        try:
            # Apply rate limiting
            await self.rate_limiter.acquire()
            
            # Submit crawl task
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/crawl",
                    json=self._build_crawl_payload(url, request),
                    headers=self._build_headers("application/json"),
                )
                response.raise_for_status()
                
                task_data = response.json()
                task_id = task_data["task_id"]
                
                # Poll for task completion
                crawl_data = await self._wait_for_task_completion(client, task_id)
                
                # Parse results with screenshot support
                return await self._parse_crawl_response(url, crawl_data, request, start_time, depth)
```

#### Recursive Crawling with URL Deduplication

```python
# services/crawling.py
def _normalize_url(self, url: str) -> str:
    """Normalize URL for deduplication."""
    parsed = urlparse(url)
    
    # Normalize path: remove trailing slash except for root
    path = parsed.path
    normalized_path = '' if path == '' or path == '/' else path.rstrip('/')
    
    # Remove fragment (everything after #)
    normalized = urlunparse((
        parsed.scheme.lower(),  # Lowercase scheme
        parsed.netloc.lower(),  # Lowercase domain
        normalized_path,        # Normalized path
        parsed.params,
        parsed.query,
        ''  # Remove fragment
    ))
    
    return normalized

async def _crawl_recursive(self, request: CrawlRequest) -> tuple[list[CrawlResult], int]:
    """Recursive crawling with breadth-first traversal."""
    results = []
    cached_count = 0
    crawled_urls = set()  # Track normalized URLs to prevent duplicates
    to_crawl = []
    
    # Initialize with seed URLs at depth 0
    for url in request.urls:
        url_str = str(url)
        normalized_url = self._normalize_url(url_str)
        parsed = urlparse(url_str)
        domain = f"{parsed.scheme}://{parsed.netloc}"
        to_crawl.append((url_str, normalized_url, 0, domain))
    
    # Crawl URLs breadth-first up to max_depth and max_pages
    while to_crawl and len(results) < request.max_pages:
        url_str, normalized_url, depth, base_domain = to_crawl.pop(0)
        
        # Skip if already crawled (check normalized URL)
        if normalized_url in crawled_urls:
            continue
        
        crawled_urls.add(normalized_url)
        
        # Process URL and add discovered links to queue...
```

#### Optimized Cache with Reverse Lookup

```python
# services/crawl_cache.py
class CrawlingCache:
    def __init__(self, ttl_hours: Optional[int] = None):
        self.ttl = timedelta(hours=ttl_hours or settings.CRAWLING_CACHE_TTL_HOURS)
        self._cache: dict[str, tuple[dict[str, Any], datetime]] = {}
        # Reverse lookup: normalized_url -> set of cache keys
        self._url_to_keys: dict[str, set[str]] = {}
    
    def _get_key(self, url: str, options: dict[str, Any]) -> str:
        """Generate cache key from URL and crawling options."""
        # Normalize URL for consistent caching
        normalized_url = self._normalize_url(url)
        
        # Include all options that affect results
        cache_data = {
            "url": normalized_url,
            "markdown_only": options.get("markdown_only", False),
            "scrape_internal_links": options.get("scrape_internal_links", False),
            "scrape_external_links": options.get("scrape_external_links", False),
            "capture_screenshots": options.get("capture_screenshots", False),
            "follow_internal_links": options.get("follow_internal_links", False),
            "follow_external_links": options.get("follow_external_links", False),
            "max_depth": options.get("max_depth", 2),
            "max_pages": options.get("max_pages", 10),
        }
        
        # Add screenshot options if capturing screenshots
        if options.get("capture_screenshots"):
            cache_data.update({
                "screenshot_width": options.get("screenshot_width", 1920),
                "screenshot_height": options.get("screenshot_height", 1080),
                "screenshot_wait_for": options.get("screenshot_wait_for", 2),
            })
        
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def invalidate_url(self, url: str) -> int:
        """Invalidate all cached results for a specific URL (O(1) operation)."""
        normalized_url = self._normalize_url(url)
        if normalized_url not in self._url_to_keys:
            return 0
        
        # Get all cache keys for this URL
        keys_to_remove = self._url_to_keys[normalized_url].copy()
        
        # Remove from main cache
        for key in keys_to_remove:
            if key in self._cache:
                del self._cache[key]
        
        # Remove from reverse lookup
        del self._url_to_keys[normalized_url]
        
        return len(keys_to_remove)
```

#### Pydantic Models with Advanced Validation

```python
# models/crawling.py
class CrawlRequest(BaseModel):
    urls: list[HttpUrl] = Field(
        ..., 
        min_length=1, 
        max_length=10,
        description="List of URLs to crawl (1-10 URLs)"
    )
    
    # Screenshot validation with 4K pixel limit
    screenshot_width: int = Field(
        default=1920,
        ge=320,
        le=3840,
        description="Screenshot viewport width in pixels (320-3840)"
    )
    screenshot_height: int = Field(
        default=1080,
        ge=240,
        le=2160,
        description="Screenshot viewport height in pixels (240-2160)"
    )
    
    @model_validator(mode='after')
    def validate_screenshot_dimensions(self) -> 'CrawlRequest':
        """Validate screenshot dimensions for security."""
        if not self.capture_screenshots:
            return self
        
        # Validate aspect ratio to prevent extreme dimensions
        aspect_ratio = self.screenshot_width / self.screenshot_height
        if aspect_ratio < 0.5 or aspect_ratio > 4.0:
            raise ValueError(
                f"Invalid aspect ratio {aspect_ratio:.2f}. "
                "Aspect ratio must be between 0.5:1 and 4:1"
            )
        
        # Validate pixel count to prevent excessive memory usage
        pixel_count = self.screenshot_width * self.screenshot_height
        if pixel_count > 8_294_400:  # 4K limit (3840 x 2160)
            raise ValueError(
                "Screenshot dimensions exceed maximum pixel count (4K resolution limit)"
            )
        
        return self
    
    @model_validator(mode='after')
    def validate_recursive_crawling(self) -> 'CrawlRequest':
        """Validate recursive crawling parameters."""
        # External link following has stricter limits for security
        if self.follow_external_links:
            if not self.scrape_external_links:
                raise ValueError("follow_external_links requires scrape_external_links")
            
            if self.max_depth > 3:
                raise ValueError("When following external links, maximum depth is 3 for security")
            
            if self.max_pages > 20:
                raise ValueError("When following external links, maximum pages is 20 for security")
        
        if self.follow_internal_links:
            if not self.scrape_internal_links:
                raise ValueError("follow_internal_links requires scrape_internal_links")
            
            # Limit seed URLs when following links to prevent exponential expansion
            if len(self.urls) > 3:
                raise ValueError("When following internal links, maximum 3 seed URLs allowed")
        
        return self
```

#### Router with Comprehensive Error Handling

```python
# routers/crawling.py
@router.post("", response_model=CrawlingResponse)
@limiter.limit(settings.CRAWLING_USER_RATE_LIMIT)
async def crawl_urls(
    request: Request,
    crawl_request: CrawlRequest,
    _api_key: str = RequiredAuth,
) -> CrawlingResponse:
    """Crawl URLs with full feature set."""
    try:
        service = get_crawling_service()
        result = await service.crawl_urls(crawl_request)
        return result

    except httpx.ConnectError as e:
        # Log the error for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Crawl4AI service unreachable: {e!s}")
        
        raise HTTPException(
            status_code=503, 
            detail="Crawl4AI service unreachable"
        ) from e
    except httpx.TimeoutException as e:
        # Log the error for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Crawl4AI service timeout: {e!s}")
        
        raise HTTPException(
            status_code=504, 
            detail="Crawl4AI service timeout"
        ) from e
    except ValidationError as e:
        # Log the error for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Invalid crawl configuration: {e!s}")
        
        raise HTTPException(
            status_code=422, 
            detail=f"Invalid crawl configuration: {e!s}"
        ) from e
    except Exception as e:
        # Log the error for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Crawling failed: {e!s}")

        raise HTTPException(
            status_code=503,
            detail=f"Crawling service temporarily unavailable: {e!s}",
        ) from e
```

### Advanced Features Implemented

#### URL Normalization for Deduplication
- **Fragment removal**: `https://example.com/page#section1` → `https://example.com/page`
- **Trailing slash normalization**: `https://example.com/page/` → `https://example.com/page`
- **Case normalization**: `HTTPS://EXAMPLE.COM` → `https://example.com`
- **Root path handling**: `https://example.com/` → `https://example.com`

#### Safety and Security Features
- **Rate limiting**: 1 req/sec to Crawl4AI, 10 req/min per user
- **Input validation**: URL format, dimension limits, parameter combinations
- **External link safety**: Stricter limits for external domain crawling
- **Memory protection**: 4K pixel limit for screenshots
- **Timeout handling**: Proper timeout management for long-running operations

#### Performance Optimizations
- **Cache invalidation**: O(1) URL-based cache invalidation with reverse lookup
- **Import placement**: Module-level imports for better performance
- **Async processing**: Full async/await pattern throughout the stack
- **Connection pooling**: Efficient HTTP client usage

### Configuration

```python
# config.py additions
CRAWL4AI_BASE_URL: str = Field(
    default="https://crawl4ai.test001.nl",
    description="Base URL for Crawl4AI instance"
)
CRAWL4AI_API_TOKEN: Optional[str] = Field(
    default=None,
    description="JWT token for Crawl4AI authentication"
)
CRAWLING_CACHE_TTL_HOURS: int = Field(
    default=1,
    description="Cache TTL for crawling results in hours"
)
CRAWLING_USER_RATE_LIMIT: str = Field(
    default="10/minute",
    description="Rate limit for users calling crawling endpoints"
)
```

### Testing Strategy

The crawling implementation includes comprehensive testing:

#### Unit Tests (59 tests)
- Service functionality with mocked HTTP clients
- Cache behavior with TTL and expiration
- URL normalization and deduplication
- Rate limiting enforcement
- Screenshot dimension validation

#### Integration Tests (31 tests)
- Full API endpoint testing
- Authentication and rate limiting
- Error handling for service downtime
- Recursive crawling behavior
- Cache integration testing

All tests are designed to work without external dependencies using comprehensive mocking strategies.

## 🤖 MCP Integration

The application includes a FastMCP server that exposes geocoding functionality through the Model Context Protocol, allowing LLM clients to access geocoding capabilities directly.

### FastMCP Server
- **Location**: `mcp/server.py`
- **Tools**: `mcp/tools/geocoding.py`
- **Integration**: Mounted at `/mcp` in main FastAPI app
- **Transport**: Streamable HTTP

### MCP Tool Pattern

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

### FastAPI Integration Pattern

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

### MCP Server Configuration Pattern

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

### Service Reuse Pattern

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

### Testing Pattern

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
```

### Key Design Principles

1. **Service Reuse**: MCP tools use identical services as REST API
2. **Singleton Pattern**: Single service instances shared across the application
3. **Proper Lifespan Management**: MCP server lifecycle integrated with FastAPI
4. **Error Handling**: Structured error responses in MCP-compatible format
5. **Testing**: Comprehensive unit and integration tests with mocking

### Dependencies Added

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

### Development Commands

```bash
# Makefile additions

test-mcp:
	source venv/bin/activate && python -c "import asyncio; from fastmcp import Client; ..."
```

### Benefits of This Implementation

1. **No Code Duplication**: Reuses all existing geocoding logic
2. **Consistent Behavior**: Same caching, rate limiting, and error handling
3. **Maintainable**: Changes to geocoding service automatically reflected in MCP
4. **Follows Architecture**: Maintains vertical slice pattern with MCP as separate module
5. **Easy to Extend**: Can add more tools later (e.g., crawling) following same pattern

## 🚀 CI/CD Pipeline Patterns

The project implements a comprehensive CI/CD pipeline using GitHub Actions with modern best practices for Python projects using uv.

### GitHub Actions Workflow Structure

```yaml
# .github/workflows/quality.yml
name: Quality & Testing

on:
  push:
    branches: [main, dev]
    paths:
      - '**.py'
      - 'pyproject.toml'
      - 'uv.lock'
      - 'Makefile'
      - '.github/workflows/**'
  pull_request:
    branches: [main, dev]
    paths:
      - '**.py'
      - 'pyproject.toml'
      - 'uv.lock'
      - 'Makefile'
      - '.github/workflows/**'
  workflow_dispatch:  # Manual trigger

env:
  UV_CACHE_DIR: /tmp/.uv-cache

jobs:
  changes:
    name: Detect Changes
    runs-on: ubuntu-latest
    outputs:
      python: ${{ steps.changes.outputs.python }}
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v3
        id: changes
        with:
          filters: |
            python:
              - '**.py'
              - 'pyproject.toml'
              - 'uv.lock'
              - 'Makefile'
```

### uv Integration Pattern

```yaml
# High-performance Python setup with uv
- name: Install uv
  uses: astral-sh/setup-uv@v6
  with:
    version: "0.8.0"
    enable-cache: true

- name: Set up Python
  run: uv python install 3.13

- name: Restore uv cache
  uses: actions/cache@v4
  with:
    path: /tmp/.uv-cache
    key: uv-${{ runner.os }}-${{ hashFiles('uv.lock') }}
    restore-keys: |
      uv-${{ runner.os }}-${{ hashFiles('uv.lock') }}
      uv-${{ runner.os }}

- name: Install dependencies
  run: uv sync

- name: Minimize uv cache
  run: uv cache prune --ci
```

### Matrix Testing Pattern

```yaml
# Test across multiple Python versions
strategy:
  fail-fast: false
  matrix:
    python-version: ["3.11", "3.12", "3.13"]

steps:
  - name: Set up Python ${{ matrix.python-version }}
    run: uv python install ${{ matrix.python-version }}
  
  - name: Run tests
    run: make test
```

### Security Workflow Pattern

```yaml
# .github/workflows/security.yml
name: Security

on:
  push:
    branches: [main, dev]
    paths:
      - '**.py'
      - 'pyproject.toml'
      - 'uv.lock'
      - 'requirements*.txt'
      - '.github/workflows/security.yml'
  pull_request:
    branches: [main, dev]
    paths:
      - '**.py'
      - 'pyproject.toml'
      - 'uv.lock'
      - 'requirements*.txt'
      - '.github/workflows/security.yml'
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday
  workflow_dispatch:

jobs:
  dependency-review:
    name: Dependency Review
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Dependency Review
        uses: actions/dependency-review-action@v4
        with:
          fail-on-severity: moderate
```

### Makefile CI Integration

```makefile
# CI-specific targets in Makefile
# Check code quality without making changes (CI-safe)
check-commit: check test
	@echo "Code quality check complete (no fixes applied)!"

# Security scanning
security:
	@echo "Running security scans..."
	uv add --dev safety bandit semgrep
	uv run safety check --json --output security-report.json
	uv run bandit -r . -f json -o bandit-report.json -x tests/
	uv run semgrep --config=auto --json --output=semgrep-report.json
```

### Path-Based Filtering

```yaml
# Only run workflows when relevant files change
paths:
  - '**.py'           # Python source files
  - 'pyproject.toml'  # Project configuration
  - 'uv.lock'         # Dependency lock file
  - 'Makefile'        # Build scripts
  - '.github/workflows/**'  # Workflow changes
```

### Artifact Management

```yaml
# Upload test and security reports
- name: Upload coverage reports
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: coverage-report
    path: htmlcov/
    retention-days: 30

- name: Upload security reports
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: security-reports
    path: |
      security-report.json
      bandit-report.json
      semgrep-report.json
    retention-days: 30
```

### Dependabot Configuration

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    reviewers:
      - "albertsikkema"
    assignees:
      - "albertsikkema"
    commit-message:
      prefix: "chore"
      include: "scope"
```

### CI/CD Best Practices

#### Performance Optimization
- **uv caching**: 10-100x faster dependency resolution
- **Path-based filtering**: Only run on relevant file changes
- **Parallel job execution**: Quality and security checks run concurrently
- **Smart cache invalidation**: Based on lock file hash

#### Security Integration
- **Dependency review**: Automated vulnerability scanning on PRs
- **Multi-tool scanning**: safety, bandit, semgrep for comprehensive analysis
- **Scheduled scans**: Weekly security checks
- **Graceful failure handling**: continue-on-error for non-critical scans

#### Development Workflow
- **CI-safe commands**: `make check-commit` (no auto-fixes in CI)
- **Local development parity**: Same commands work locally and in CI
- **Comprehensive testing**: 160 tests across unit, integration, and security
- **Matrix testing**: Python 3.11, 3.12, 3.13 compatibility

### Key Files

- `.github/workflows/quality.yml`: Main quality and testing workflow
- `.github/workflows/security.yml`: Security scanning workflow
- `.github/dependabot.yml`: Dependency update configuration
- `Makefile`: CI/CD command definitions (check-commit, security, etc.)

### Status Checks for Branch Protection

```yaml
# Recommended required status checks
required_status_checks:
  strict: true
  contexts:
    - "Quality & Testing / Code Quality"
    - "Quality & Testing / Test Matrix (3.11)"
    - "Quality & Testing / Test Matrix (3.12)"  
    - "Quality & Testing / Test Matrix (3.13)"
    - "Quality & Testing / Build Check"
    - "Security / Dependency Review"
```

### Migration from pip to uv

The project successfully migrated from pip to uv for:
- **Faster builds**: 10-100x improvement in dependency resolution
- **Better caching**: More efficient cache management
- **Unified tooling**: Single tool for dependencies, virtual environments, and execution
- **Modern Python packaging**: Following 2025 best practices

**Key Benefits Achieved:**
1. Dramatically faster CI/CD pipelines
2. Consistent environments across development and production
3. Better dependency resolution and conflict detection
4. Improved developer experience with faster local development
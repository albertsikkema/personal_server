# PRP: Geocoding Endpoint Implementation

## Feature: Create an endpoint that accepts a city name (string) as a query and returns a location (lat, lon)

### Overview
Implement a geocoding endpoint that converts city names to geographic coordinates using the Nominatim API. The endpoint will follow existing FastAPI patterns and include comprehensive error handling, validation, and testing. **CRITICAL: Must adhere to Nominatim rate limits (max 1 request per second).**

### Context & Documentation

#### Nominatim API Documentation
- **Python Library**: https://nominatim.org/release-docs/latest/library/Getting-Started/
- **Search API**: https://nominatim.org/release-docs/latest/api/Search/
- **Rate Limiting**: https://operations.osmfoundation.org/policies/nominatim/

#### Nominatim Usage Policy (MUST FOLLOW)
From https://operations.osmfoundation.org/policies/nominatim/:
- **Absolute maximum of 1 request per second**
- **Provide a valid HTTP Referer or User-Agent**
- **Clearly display attribution**
- **Cache results whenever possible**
- **No heavy uses (>1 request/sec) - will result in IP ban**

#### Key Nominatim Code Examples
```python
# Async search from ai_info/docs/nominatim.md:42-56
import asyncio
import nominatim_api as napi

async def search(query):
    async with napi.NominatimAPIAsync() as api:
        return await api.search(query)

results = asyncio.run(search('Brugge'))
if not results:
    print('Cannot find Brugge')
else:
    print(f'Found a place at {results[0].centroid.x},{results[0].centroid.y}')
```

### Existing Codebase Patterns

#### Endpoint Pattern (from main.py:72-87)
```python
@app.get("/protected")
async def protected_endpoint(_api_key: str = RequiredAuth):
    """
    Protected endpoint that requires API key authentication.
    Authentication is handled by dependency injection.

    Args:
        api_key: The validated API key from the dependency

    Returns:
        A message confirming access to protected resource
    """
    return {
        "message": "Access granted to protected resource",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
```

#### Configuration Pattern (from config.py)
```python
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        validate_default=True,
    )
```

### Implementation Blueprint

#### 1. Pydantic Models
```python
# models/geocoding.py
from pydantic import BaseModel, Field
from typing import Optional, List

class GeocodingRequest(BaseModel):
    city: str = Field(..., min_length=1, max_length=200, description="City name to geocode")

class Location(BaseModel):
    lat: float = Field(..., description="Latitude")
    lon: float = Field(..., description="Longitude")
    
class GeocodingResponse(BaseModel):
    city: str = Field(..., description="Requested city name")
    location: Location = Field(..., description="Geographic coordinates")
    display_name: str = Field(..., description="Full formatted address")
    place_id: Optional[int] = Field(None, description="Nominatim place ID")
    boundingbox: Optional[List[float]] = Field(None, description="Bounding box [min_lat, max_lat, min_lon, max_lon]")
    timestamp: str = Field(..., description="Response timestamp in ISO format")
    cached: bool = Field(default=False, description="Whether this result was from cache")
```

#### 2. Rate Limiter Module
```python
# services/rate_limiter.py
import asyncio
import time
from typing import Optional
from datetime import datetime, timedelta
from utils.logging import get_logger

logger = get_logger(__name__)

class RateLimiter:
    """Rate limiter to ensure Nominatim API limits are respected."""
    
    def __init__(self, max_requests: int = 1, time_window: float = 1.0):
        self.max_requests = max_requests
        self.time_window = time_window  # in seconds
        self.last_request_time: Optional[float] = None
        self._lock = asyncio.Lock()
    
    async def acquire(self):
        """Ensure rate limit is not exceeded. Blocks if necessary."""
        async with self._lock:
            current_time = time.time()
            
            if self.last_request_time is not None:
                time_since_last = current_time - self.last_request_time
                if time_since_last < self.time_window:
                    sleep_time = self.time_window - time_since_last
                    logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f}s")
                    await asyncio.sleep(sleep_time)
            
            self.last_request_time = time.time()
```

#### 3. Cache Module
```python
# services/cache.py
from typing import Optional, Dict
import hashlib
from datetime import datetime, timedelta
from utils.logging import get_logger

logger = get_logger(__name__)

class GeocodingCache:
    """In-memory cache for geocoding results to minimize API calls."""
    
    def __init__(self, ttl_hours: int = 24):
        self._cache: Dict[str, tuple[dict, datetime]] = {}
        self.ttl = timedelta(hours=ttl_hours)
    
    def _get_key(self, city: str) -> str:
        """Generate cache key from city name."""
        return hashlib.md5(city.lower().strip().encode()).hexdigest()
    
    def get(self, city: str) -> Optional[dict]:
        """Get cached result if exists and not expired."""
        key = self._get_key(city)
        if key in self._cache:
            data, timestamp = self._cache[key]
            if datetime.now() - timestamp < self.ttl:
                logger.info(f"Cache hit for city: {city}")
                return data
            else:
                del self._cache[key]
                logger.debug(f"Cache expired for city: {city}")
        return None
    
    def set(self, city: str, data: dict):
        """Cache a geocoding result."""
        key = self._get_key(city)
        self._cache[key] = (data, datetime.now())
        logger.debug(f"Cached result for city: {city}")
```

#### 4. Service Module with Rate Limiting
```python
# services/geocoding.py
import nominatim_api as napi
from typing import Optional
from models.geocoding import Location, GeocodingResponse
from services.rate_limiter import RateLimiter
from services.cache import GeocodingCache
from datetime import datetime, timezone
from utils.logging import get_logger
from config import settings

logger = get_logger(__name__)

class GeocodingService:
    def __init__(self):
        self.rate_limiter = RateLimiter(max_requests=1, time_window=1.0)
        self.cache = GeocodingCache(ttl_hours=settings.GEOCODING_CACHE_TTL_HOURS)
        self.user_agent = f"{settings.APP_NAME}/1.0"
        
    async def geocode_city(self, city: str) -> Optional[GeocodingResponse]:
        """
        Geocode a city name to coordinates using Nominatim.
        Implements caching and rate limiting to respect API limits.
        
        Args:
            city: City name to geocode
            
        Returns:
            GeocodingResponse or None if not found
        """
        # Check cache first
        cached = self.cache.get(city)
        if cached:
            response = GeocodingResponse(**cached)
            response.cached = True
            return response
        
        # Rate limit before API call
        await self.rate_limiter.acquire()
        
        try:
            # Set User-Agent as required by Nominatim policy
            async with napi.NominatimAPIAsync(
                user_agent=self.user_agent
            ) as api:
                results = await api.search(city, address_details=True)
                
                if not results:
                    logger.info(f"No results found for city: {city}")
                    return None
                    
                # Use first result
                result = results[0]
                
                response = GeocodingResponse(
                    city=city,
                    location=Location(
                        lat=result.centroid.y,
                        lon=result.centroid.x
                    ),
                    display_name=result.display_name,
                    place_id=result.place_id,
                    boundingbox=result.boundingbox if hasattr(result, 'boundingbox') else None,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    cached=False
                )
                
                # Cache the result
                self.cache.set(city, response.model_dump())
                
                return response
                
        except Exception as e:
            logger.error(f"Geocoding error for city '{city}': {str(e)}")
            raise
```

#### 5. Geocoding Router Implementation
```python
# routers/geocoding.py
from fastapi import APIRouter, Query, Request, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from models.geocoding import GeocodingResponse
from services.geocoding import GeocodingService
from dependencies import RequiredAuth
from utils.logging import get_logger

logger = get_logger(__name__)

# Initialize limiter for this router
limiter = Limiter(key_func=get_remote_address)

# Create router
router = APIRouter(
    prefix="/geocode",
    tags=["geocoding"],
    dependencies=[RequiredAuth],  # Apply auth to all routes in this router
)

# Initialize service
geocoding_service = GeocodingService()

@router.get("/city", response_model=GeocodingResponse)
@limiter.limit("10/minute")  # User rate limit
async def geocode_city(
    request: Request,  # Required for rate limiter
    city: str = Query(
        ..., 
        min_length=1, 
        max_length=200, 
        description="City name to geocode",
        example="London"
    ),
):
    """
    Geocode a city name to geographic coordinates.
    
    This endpoint uses the Nominatim geocoding service to convert
    city names into latitude and longitude coordinates.
    
    Rate limits:
    - User limit: 10 requests per minute
    - Nominatim API: 1 request per second (handled internally)
    
    Args:
        request: FastAPI request object (for rate limiting)
        city: The name of the city to geocode
        
    Returns:
        Geographic coordinates and location details
        
    Raises:
        HTTPException: If city not found or geocoding fails
        RateLimitExceeded: If user exceeds rate limit
    """
    logger.info(f"Geocoding request for city: {city}")
    
    try:
        result = await geocoding_service.geocode_city(city)
        
        if not result:
            logger.warning(f"City not found: {city}")
            raise HTTPException(
                status_code=404,
                detail=f"City '{city}' not found"
            )
        
        logger.info(f"Geocoding successful for city: {city}, cached: {result.cached}")
        return result
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except Exception as e:
        logger.error(f"Geocoding service error for city '{city}': {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="Geocoding service temporarily unavailable"
        )

@router.get("/health")
async def geocoding_health():
    """
    Health check endpoint for geocoding service.
    
    Returns:
        Service health status
    """
    return {
        "service": "geocoding",
        "status": "healthy",
        "cache_size": len(geocoding_service.cache._cache),
        "rate_limiter": "active"
    }
```

#### 6. Router Registration in Main App
```python
# In main.py, add:
from routers import geocoding
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Initialize global limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include routers
app.include_router(
    geocoding.router,
    responses={
        401: {"description": "Authentication required"},
        404: {"description": "City not found"},
        429: {"description": "Rate limit exceeded"},
        503: {"description": "Service unavailable"}
    }
)
```

#### 7. Router Module Structure
```python
# routers/__init__.py
"""
FastAPI routers for organizing endpoints by feature.
"""

# Import all routers here for easy access
from . import geocoding

__all__ = ["geocoding"]
```

#### 8. Configuration Updates
```python
# config.py additions
GEOCODING_CACHE_TTL_HOURS: int = Field(
    default=24,
    description="Cache TTL for geocoding results in hours"
)
GEOCODING_USER_RATE_LIMIT: str = Field(
    default="10/minute",
    description="Rate limit for users calling geocoding endpoint"
)
```

### Error Handling Strategy

1. **City Not Found**: Return 404 with clear message
2. **Nominatim API Error**: Return 503 Service Unavailable
3. **Invalid Input**: Handled by Pydantic validation (400 Bad Request)
4. **Rate Limiting**: Return 429 Too Many Requests with retry-after header

### Testing Strategy (TDD Approach)

**IMPORTANT: Start with tests first (Test-Driven Development)**

#### 1. Unit Tests (Create FIRST)
```python
# tests/test_rate_limiter.py
import pytest
import asyncio
import time
from services.rate_limiter import RateLimiter

@pytest.mark.asyncio
async def test_rate_limiter_allows_first_request():
    """Test that first request is allowed immediately."""
    limiter = RateLimiter(max_requests=1, time_window=1.0)
    
    start_time = time.time()
    await limiter.acquire()
    elapsed = time.time() - start_time
    
    assert elapsed < 0.1  # Should be nearly instant

@pytest.mark.asyncio
async def test_rate_limiter_enforces_delay():
    """Test that second request is delayed appropriately."""
    limiter = RateLimiter(max_requests=1, time_window=1.0)
    
    # First request
    await limiter.acquire()
    
    # Second request should be delayed
    start_time = time.time()
    await limiter.acquire()
    elapsed = time.time() - start_time
    
    assert elapsed >= 0.9  # Should wait close to 1 second

# tests/test_cache.py
import pytest
from services.cache import GeocodingCache
from datetime import datetime, timedelta

def test_cache_stores_and_retrieves():
    """Test basic cache functionality."""
    cache = GeocodingCache(ttl_hours=1)
    
    test_data = {"lat": 52.5, "lon": 13.4}
    cache.set("Berlin", test_data)
    
    result = cache.get("Berlin")
    assert result == test_data

def test_cache_expiry():
    """Test that expired entries are removed."""
    cache = GeocodingCache(ttl_hours=1)
    cache.set("Berlin", {"lat": 52.5, "lon": 13.4})
    
    # Manually expire the entry
    key = cache._get_key("Berlin")
    old_time = datetime.now() - timedelta(hours=2)
    cache._cache[key] = (cache._cache[key][0], old_time)
    
    result = cache.get("Berlin")
    assert result is None

# tests/test_geocoding_service.py
import pytest
from unittest.mock import AsyncMock, patch
from services.geocoding import GeocodingService

@pytest.mark.asyncio
async def test_geocode_city_success():
    """Test successful geocoding."""
    service = GeocodingService()
    
    # Mock Nominatim response
    mock_result = AsyncMock()
    mock_result.centroid.x = 13.404954
    mock_result.centroid.y = 52.520008
    mock_result.display_name = "Berlin, Germany"
    mock_result.place_id = 12345
    
    with patch('nominatim_api.NominatimAPIAsync') as mock_api:
        mock_api.return_value.__aenter__.return_value.search.return_value = [mock_result]
        
        result = await service.geocode_city("Berlin")
        
        assert result.location.lat == 52.520008
        assert result.location.lon == 13.404954
        assert result.city == "Berlin"
        assert result.cached is False

@pytest.mark.asyncio
async def test_geocode_city_cache_hit():
    """Test that cached results are returned."""
    service = GeocodingService()
    
    # First call with mock
    mock_result = AsyncMock()
    mock_result.centroid.x = 13.404954
    mock_result.centroid.y = 52.520008
    mock_result.display_name = "Berlin, Germany"
    mock_result.place_id = 12345
    
    with patch('nominatim_api.NominatimAPIAsync') as mock_api:
        mock_api.return_value.__aenter__.return_value.search.return_value = [mock_result]
        
        # First call
        result1 = await service.geocode_city("Berlin")
        
        # Second call should hit cache (no API call)
        result2 = await service.geocode_city("Berlin")
        
        assert result2.cached is True
        assert result1.location.lat == result2.location.lat
        # API should only be called once
        assert mock_api.call_count == 1

@pytest.mark.asyncio
async def test_rate_limiting_in_service():
    """Test that rate limiting is enforced in service."""
    service = GeocodingService()
    
    mock_result = AsyncMock()
    mock_result.centroid.x = 13.404954
    mock_result.centroid.y = 52.520008
    mock_result.display_name = "Berlin, Germany"
    mock_result.place_id = 12345
    
    with patch('nominatim_api.NominatimAPIAsync') as mock_api:
        mock_api.return_value.__aenter__.return_value.search.return_value = [mock_result]
        
        # Clear cache to ensure API calls
        service.cache._cache.clear()
        
        start_time = time.time()
        
        # Two different cities to avoid cache
        await service.geocode_city("Berlin")
        await service.geocode_city("London")
        
        elapsed = time.time() - start_time
        
        # Should take at least 1 second due to rate limiting
        assert elapsed >= 1.0
```

#### 2. Integration Tests (Create SECOND)
```python
# tests/test_integration.py additions
import time

def test_geocode_city_success(client: TestClient, valid_api_key: str):
    """Test successful city geocoding."""
    response = client.get(
        "/geocode/city?city=London",
        headers={"X-API-KEY": valid_api_key}
    )
    assert response.status_code == 200
    data = response.json()
    assert "location" in data
    assert "lat" in data["location"]
    assert "lon" in data["location"]
    assert data["city"] == "London"
    assert "cached" in data
    assert "timestamp" in data

def test_geocode_city_not_found(client: TestClient, valid_api_key: str):
    """Test geocoding with non-existent city."""
    response = client.get(
        "/geocode/city?city=Xyzabcdef123NonExistentCity",
        headers={"X-API-KEY": valid_api_key}
    )
    assert response.status_code == 404
    data = response.json()
    assert "City 'Xyzabcdef123NonExistentCity' not found" in data["detail"]

def test_geocode_health_endpoint(client: TestClient, valid_api_key: str):
    """Test geocoding health endpoint."""
    response = client.get(
        "/geocode/health",
        headers={"X-API-KEY": valid_api_key}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "geocoding"
    assert data["status"] == "healthy"
    assert "cache_size" in data
    assert data["rate_limiter"] == "active"

def test_geocode_rate_limiting(client: TestClient, valid_api_key: str):
    """Test user rate limiting."""
    # Make multiple rapid requests
    for i in range(11):  # Exceed 10/minute limit
        response = client.get(
            f"/geocode/city?city=TestCity{i}",
            headers={"X-API-KEY": valid_api_key}
        )
        if i < 10:
            assert response.status_code in [200, 404]  # Normal responses
        else:
            assert response.status_code == 429  # Rate limited

def test_geocode_caching_behavior(client: TestClient, valid_api_key: str):
    """Test that caching works correctly."""
    # First request
    response1 = client.get(
        "/geocode/city?city=Paris",
        headers={"X-API-KEY": valid_api_key}
    )
    assert response.status_code == 200
    data1 = response1.json()
    assert data1["cached"] is False
    
    # Second request should be cached
    response2 = client.get(
        "/geocode/city?city=Paris",
        headers={"X-API-KEY": valid_api_key}
    )
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["cached"] is True
    assert data1["location"] == data2["location"]

def test_geocode_authentication_required(client: TestClient):
    """Test that authentication is required."""
    response = client.get("/geocode/city?city=London")
    assert response.status_code == 401

def test_geocode_invalid_input(client: TestClient, valid_api_key: str):
    """Test input validation."""
    # Empty city name
    response = client.get(
        "/geocode/city?city=",
        headers={"X-API-KEY": valid_api_key}
    )
    assert response.status_code == 422
    
    # City name too long (>200 chars)
    long_city = "x" * 201
    response = client.get(
        f"/geocode/city?city={long_city}",
        headers={"X-API-KEY": valid_api_key}
    )
    assert response.status_code == 422

def test_geocode_router_tags_and_prefix(client: TestClient):
    """Test that router is properly configured with prefix and tags."""
    # Check OpenAPI schema includes router configuration
    response = client.get("/openapi.json")
    assert response.status_code == 200
    openapi_schema = response.json()
    
    # Verify geocoding endpoints are under /geocode prefix
    assert "/geocode/city" in openapi_schema["paths"]
    assert "/geocode/health" in openapi_schema["paths"]
    
    # Verify tags are applied
    city_endpoint = openapi_schema["paths"]["/geocode/city"]["get"]
    assert "geocoding" in city_endpoint["tags"]
```

#### 3. Router Tests (Create THIRD)
```python
# tests/test_router.py
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from routers.geocoding import router

def test_router_creation():
    """Test that router is properly configured."""
    assert router.prefix == "/geocode"
    assert "geocoding" in router.tags
    assert len(router.dependencies) > 0  # Auth dependency should be present

@pytest.fixture
def app_with_router():
    """Create test app with only geocoding router."""
    app = FastAPI()
    app.include_router(router)
    return app

def test_router_endpoints_registered(app_with_router):
    """Test that all router endpoints are registered."""
    client = TestClient(app_with_router)
    
    # Test that endpoints exist (will return 401 without auth)
    response = client.get("/geocode/city?city=London")
    assert response.status_code == 401  # Auth required
    
    response = client.get("/geocode/health")
    assert response.status_code == 401  # Auth required
```

### Implementation Tasks (TDD Order)

**Phase 1: Setup Dependencies**
1. **Add required dependencies**
   - Add `nominatim-api` to requirements.txt
   - Add `slowapi` for rate limiting to requirements.txt
   - Update pyproject.toml

**Phase 2: Tests First (TDD)**
2. **Create test files FIRST**
   - Create tests/test_rate_limiter.py with rate limiting tests
   - Create tests/test_cache.py with caching tests
   - Create tests/test_geocoding_service.py with service tests
   - Add integration tests to tests/test_integration.py

**Phase 3: Implementation to Pass Tests**
3. **Create models module**
   - Create models/__init__.py
   - Create models/geocoding.py with Pydantic models

4. **Create rate limiter module**
   - Create services/__init__.py
   - Create services/rate_limiter.py with RateLimiter class

5. **Create cache module**
   - Create services/cache.py with GeocodingCache class

6. **Create geocoding service**
   - Create services/geocoding.py with GeocodingService
   - Implement rate limiting and caching

7. **Create router module**
   - Create routers/__init__.py
   - Create routers/geocoding.py with APIRouter
   - Implement geocoding endpoints with rate limiting

8. **Update configuration**
   - Add geocoding settings to config.py

9. **Update main.py**
   - Import geocoding router
   - Register router with app.include_router()
   - Add rate limiting middleware

**Phase 4: Documentation**
10. **Update documentation**
   - Add endpoint to README.md
   - Update Claude.md with router patterns
   - Document rate limiting policies

### Validation Gates

```bash
# Syntax/Style Check
ruff check --fix . && ruff format .

# Type Checking (if mypy is configured)
# mypy .

# Run All Tests
pytest tests/ -v

# Run with Coverage
pytest --cov=. --cov-report=term-missing

# Full Quality Check
make quality
```

### Gotchas & Considerations

#### Rate Limiting (CRITICAL)
1. **Nominatim Policy Compliance**:
   - **NEVER exceed 1 request per second** - will result in IP ban
   - Must provide User-Agent header in all requests
   - Test with mock data to avoid hitting real API during development
   - Use separate test cities to avoid cache interference

2. **Implementation Details**:
   - RateLimiter must use asyncio.Lock for thread safety
   - Cache keys should be case-insensitive and normalized
   - Error handling must not bypass rate limiting

#### Testing Considerations
3. **TDD Best Practices**:
   - Write failing tests first, then implement
   - Mock Nominatim API calls in unit tests
   - Use `time.sleep()` tests sparingly (slow tests)
   - Test rate limiting with separate instances

#### API Design
4. **Multiple Results**: Nominatim may return multiple results for a city name. Current implementation uses the first result.

5. **Internationalization**: City names can be in different languages and scripts. Ensure proper Unicode handling.

6. **Performance**: 
   - Cache hits should be <100ms
   - API calls will be >1s due to rate limiting
   - User rate limiting prevents abuse

### Success Criteria

- [ ] **All tests pass (TDD approach)**
- [ ] **Rate limiting enforced (max 1 req/sec to Nominatim)**
- [ ] **Caching reduces API calls**
- [ ] **User rate limiting works (10/minute)**
- [ ] Endpoint accepts city name and returns coordinates
- [ ] Proper error handling for all edge cases
- [ ] Comprehensive test coverage (>90%)
- [ ] Documentation updated
- [ ] All validation gates pass
- [ ] Nominatim attribution displayed

### Rate Limiting Validation Checklist

**MUST TEST THESE:**
- [ ] RateLimiter enforces 1-second delay between API calls
- [ ] Cache prevents unnecessary API calls
- [ ] User rate limiting returns 429 after 10 requests/minute
- [ ] User-Agent header is sent with all Nominatim requests
- [ ] Tests use mocks, not real Nominatim API
- [ ] Integration tests respect actual rate limits

### Confidence Score: 9/10

High confidence in successful implementation due to:
- Clear documentation and examples
- Well-established patterns in codebase
- Comprehensive rate limiting strategy
- TDD approach ensures correctness
- Detailed testing strategy

**Risk mitigation:**
- Rate limiting implementation thoroughly tested
- Cache reduces API dependency
- Mock tests prevent API abuse during development
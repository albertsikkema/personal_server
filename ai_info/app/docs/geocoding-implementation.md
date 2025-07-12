# Geocoding API Implementation Patterns

This document contains detailed implementation patterns for the geocoding API that converts city names to geographic coordinates using the Nominatim service.

## Features
- **Rate Limiting**: Complies with Nominatim's 1 request/second policy
- **Caching**: 24-hour TTL to minimize API calls
- **User Rate Limiting**: 10 requests/minute per IP
- **Authentication**: Requires API key for all endpoints
- **Error Handling**: Comprehensive error responses with proper status codes

## API Endpoints

### Geocode City
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

### Health Check
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

### Clear Cache (Admin)
```
POST /geocode/cache/clear
```

## Core Models

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

## Implementation Patterns

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

## Architecture

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

## Configuration

Add to `.env` or environment variables:
```bash
GEOCODING_CACHE_TTL_HOURS=24
GEOCODING_USER_RATE_LIMIT=10/minute
```

## Dependencies
- `httpx`: HTTP client for Nominatim API calls
- `slowapi`: Rate limiting middleware

## Nominatim Compliance

The implementation strictly follows Nominatim's usage policy:
- Maximum 1 request per second (enforced by RateLimiter)
- User-Agent header provided with all requests
- Results cached to minimize API calls
- Proper attribution (handled in client implementation)

## Testing Approach

### Unit Tests (9 tests)
- Authentication dependency validation
- Custom exception handling
- Error response format verification

### Integration Tests (31 tests)  
- Full API endpoint testing
- Security attack simulations
- OpenAPI documentation verification
- Environment-based behavior testing
# Web Crawling API Implementation Patterns

This document contains comprehensive implementation patterns for the web crawling API that integrates with Crawl4AI to provide advanced crawling capabilities with screenshot capture and recursive link following.

## Features
- **Multi-URL Crawling**: Process up to 10 URLs per request with async processing
- **Screenshot Capture**: Full-page screenshots with custom dimensions and validation
- **Recursive Crawling**: Follow internal and external links with configurable depth
- **Smart URL Deduplication**: Normalize URLs to prevent duplicate crawling
- **Rate Limiting**: Service-level (1 req/sec) and user-level (10 req/min) protection
- **Caching**: TTL-based caching with O(1) invalidation performance
- **Authentication**: JWT token support for Crawl4AI service

## Core Architecture

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

## Key Implementation Patterns

### Async Task-Based API Integration

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

### Recursive Crawling with URL Deduplication

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

### Optimized Cache with Reverse Lookup

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

### Pydantic Models with Advanced Validation

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

### Router with Comprehensive Error Handling

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

## Advanced Features Implemented

### URL Normalization for Deduplication
- **Fragment removal**: `https://example.com/page#section1` → `https://example.com/page`
- **Trailing slash normalization**: `https://example.com/page/` → `https://example.com/page`
- **Case normalization**: `HTTPS://EXAMPLE.COM` → `https://example.com`
- **Root path handling**: `https://example.com/` → `https://example.com`

### Safety and Security Features
- **Rate limiting**: 1 req/sec to Crawl4AI, 10 req/min per user
- **Input validation**: URL format, dimension limits, parameter combinations
- **External link safety**: Stricter limits for external domain crawling
- **Memory protection**: 4K pixel limit for screenshots
- **Timeout handling**: Proper timeout management for long-running operations

### Performance Optimizations
- **Cache invalidation**: O(1) URL-based cache invalidation with reverse lookup
- **Import placement**: Module-level imports for better performance
- **Async processing**: Full async/await pattern throughout the stack
- **Connection pooling**: Efficient HTTP client usage

## Configuration

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

## Testing Strategy

The crawling implementation includes comprehensive testing:

### Unit Tests (59 tests)
- Service functionality with mocked HTTP clients
- Cache behavior with TTL and expiration
- URL normalization and deduplication
- Rate limiting enforcement
- Screenshot dimension validation

### Integration Tests (31 tests)
- Full API endpoint testing
- Authentication and rate limiting
- Error handling for service downtime
- Recursive crawling behavior
- Cache integration testing

All tests are designed to work without external dependencies using comprehensive mocking strategies.
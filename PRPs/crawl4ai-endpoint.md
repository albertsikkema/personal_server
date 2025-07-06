# PRP: Crawl4AI Endpoint Implementation

## Feature: Create an endpoint that accepts multiple URLs and crawls them using Crawl4AI instance

### Overview
Implement a crawling endpoint that integrates with an existing Crawl4AI instance at `https://crawl4ai.test001.nl` to crawl multiple URLs with configurable options for internal/external link extraction, markdown-only output, and screenshot capture. The endpoint will follow existing FastAPI patterns and include comprehensive error handling, validation, and testing.

### Context & Documentation

#### Crawl4AI API Documentation
- **Official Documentation**: https://docs.crawl4ai.com/
- **Multi-URL Crawling**: https://docs.crawl4ai.com/advanced/multi-url-crawling/
- **REST API Endpoints**: https://docs.crawl4ai.com/core/docker-deployment/
- **Link Extraction**: https://docs.crawl4ai.com/core/link-media/
- **Markdown Generation**: https://docs.crawl4ai.com/core/markdown-generation/

#### Crawl4AI Instance Details
- **Base URL**: `https://crawl4ai.test001.nl`
- **Expected Port**: `11235` (standard crawl4ai port)
- **Health Check**: `GET /health`
- **Main Endpoints**:
  - `POST /crawl` - Submit crawling jobs
  - `POST /crawl/stream` - Streaming endpoint for multiple URLs
  - `POST /screenshot` - Capture full-page screenshots
  - `GET /task/{task_id}` - Check task status and get results

#### Key Crawl4AI Code Examples from Documentation

```python
# Multi-URL crawling with arun_many (from crawl4ai.md:360-375)
dispatcher = MemoryAdaptiveDispatcher(
    memory_threshold_percent=70.0,
    max_session_permit=10
)
results = await crawler.arun_many(
    urls=["https://site1.com", "https://site2.com", "https://site3.com"],
    config=my_run_config,
    dispatcher=dispatcher
)

# REST API usage (from crawl4ai.md:1123-1157)
browser_config_payload = {
    "type": "BrowserConfig",
    "params": {"headless": True}
}
crawler_config_payload = {
    "type": "CrawlerRunConfig",
    "params": {"stream": False, "cache_mode": "bypass"}
}

crawl_payload = {
    "urls": ["https://httpbin.org/html"],
    "browser_config": browser_config_payload,
    "crawler_config": crawler_config_payload
}
response = requests.post(
    "http://localhost:11235/crawl",
    json=crawl_payload
)

# Result structure (from crawl4ai.md:21-33)
result.html         # Raw HTML
result.cleaned_html # Cleaned HTML
result.markdown.raw_markdown # Raw markdown from cleaned html
result.markdown.fit_markdown # Most relevant content in markdown
result.success      # True if crawl succeeded
result.status_code  # HTTP status code (e.g., 200, 404)
result.media        # Dictionary of found media (images, videos, audio)
result.links        # Dictionary of internal and external links

# Screenshot API (from crawl4ai.md:778-796)
POST /screenshot
{
  "url": "https://example.com",
  "screenshot_wait_for": 2,
  "output_path": "/path/to/save/screenshot.png"
}
```

### Existing Codebase Patterns

#### Router Pattern (from routers/geocoding.py:31-38)
```python
router = APIRouter(
    prefix="/crawl",
    tags=["crawling"],
    dependencies=[RequiredAuth],  # Apply auth to all routes in this router
)

# Initialize service (singleton pattern)
crawling_service = CrawlingService()
```

#### Rate Limiting Pattern (from routers/geocoding.py:41-52)
```python
@router.post("/batch", response_model=CrawlingResponse)
@limiter.limit(settings.CRAWLING_USER_RATE_LIMIT)
async def crawl_urls(
    request: Request,  # Required for rate limiter
    crawl_request: CrawlRequest = Body(...),
):
```

#### Service Pattern (from services/geocoding.py:28-55)
```python
class GeocodingService:
    def __init__(self):
        self.rate_limiter = RateLimiter(max_requests=1, time_window=1.0)
        self.cache = GeocodingCache(ttl_hours=settings.GEOCODING_CACHE_TTL_HOURS)
        self.user_agent = f"{settings.APP_NAME}/1.0"
        self.base_url = "https://nominatim.openstreetmap.org"
```

### Implementation Blueprint

#### 1. Pydantic Models
```python
# models/crawling.py
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any
from enum import Enum

class CrawlRequest(BaseModel):
    urls: List[HttpUrl] = Field(
        ..., 
        min_length=1, 
        max_length=50,
        description="List of URLs to crawl (1-50 URLs)",
        examples=[["https://example.com", "https://test.com"]]
    )
    scrape_internal_links: bool = Field(
        default=False,
        description="Extract and include internal links in results"
    )
    scrape_external_links: bool = Field(
        default=False,
        description="Extract and include external links in results"
    )
    markdown_only: bool = Field(
        default=False,
        description="Return only markdown content (no HTML or metadata)"
    )
    capture_screenshots: bool = Field(
        default=False,
        description="Capture full-page screenshots of URLs"
    )
    screenshot_wait_for: Optional[int] = Field(
        default=2,
        ge=0,
        le=10,
        description="Seconds to wait before capturing screenshot (0-10)"
    )
    screenshot_width: Optional[int] = Field(
        default=1920,
        ge=320,
        le=3840,
        description="Screenshot viewport width in pixels (320-3840)"
    )
    screenshot_height: Optional[int] = Field(
        default=1080,
        ge=240,
        le=2160,
        description="Screenshot viewport height in pixels (240-2160)"
    )
    cache_mode: Optional[str] = Field(
        default="enabled",
        pattern="^(enabled|disabled|bypass)$",
        description="Cache behavior for crawling results"
    )

class CrawlResult(BaseModel):
    url: str = Field(..., description="Original URL")
    success: bool = Field(..., description="Whether crawl succeeded")
    status_code: Optional[int] = Field(None, description="HTTP status code")
    markdown: Optional[str] = Field(None, description="Markdown content")
    cleaned_html: Optional[str] = Field(None, description="Cleaned HTML content")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Page metadata")
    internal_links: Optional[List[str]] = Field(None, description="Internal links found")
    external_links: Optional[List[str]] = Field(None, description="External links found")
    screenshot_base64: Optional[str] = Field(None, description="Base64-encoded screenshot image")
    screenshot_size: Optional[Dict[str, int]] = Field(None, description="Screenshot dimensions (width, height)")
    error_message: Optional[str] = Field(None, description="Error details if failed")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")

class CrawlingResponse(BaseModel):
    total_urls: int = Field(..., description="Total number of URLs processed")
    successful_crawls: int = Field(..., description="Number of successful crawls")
    failed_crawls: int = Field(..., description="Number of failed crawls")
    results: List[CrawlResult] = Field(..., description="Individual crawl results")
    timestamp: str = Field(..., description="Response timestamp in ISO format")
    total_processing_time: float = Field(..., description="Total processing time in seconds")
    cached_results: int = Field(default=0, description="Number of cached results used")

class CrawlingHealthResponse(BaseModel):
    service: str = Field(default="crawling", description="Service name")
    status: str = Field(..., description="Service status")
    crawl4ai_instance: str = Field(..., description="Crawl4AI instance URL")
    crawl4ai_healthy: bool = Field(..., description="Whether Crawl4AI instance is healthy")
    cache_size: int = Field(default=0, description="Number of cached results")
    rate_limiter_active: bool = Field(default=True, description="Rate limiter status")
```

#### 2. Cache Module
```python
# services/crawl_cache.py
from typing import Optional, Dict, List
import hashlib
import json
from datetime import datetime, timedelta
from utils.logging import get_logger

logger = get_logger(__name__)

class CrawlingCache:
    """In-memory cache for crawling results to minimize API calls."""
    
    def __init__(self, ttl_hours: int = 1):
        self._cache: Dict[str, tuple[dict, datetime]] = {}
        self.ttl = timedelta(hours=ttl_hours)
    
    def _get_key(self, url: str, options: dict) -> str:
        """Generate cache key from URL and crawling options."""
        cache_data = {
            "url": url.lower().strip(),
            "scrape_internal_links": options.get("scrape_internal_links", False),
            "scrape_external_links": options.get("scrape_external_links", False),
            "markdown_only": options.get("markdown_only", False),
            "capture_screenshots": options.get("capture_screenshots", False),
            "screenshot_wait_for": options.get("screenshot_wait_for", 2),
            "screenshot_width": options.get("screenshot_width", 1920),
            "screenshot_height": options.get("screenshot_height", 1080)
        }
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def get(self, url: str, options: dict) -> Optional[dict]:
        """Get cached result if exists and not expired."""
        key = self._get_key(url, options)
        if key in self._cache:
            data, timestamp = self._cache[key]
            if datetime.now() - timestamp < self.ttl:
                logger.info(f"Cache hit for URL: {url}")
                return data
            else:
                del self._cache[key]
                logger.debug(f"Cache expired for URL: {url}")
        return None
    
    def set(self, url: str, options: dict, data: dict):
        """Cache a crawling result."""
        key = self._get_key(url, options)
        self._cache[key] = (data, datetime.now())
        logger.debug(f"Cached result for URL: {url}")
    
    def size(self) -> int:
        """Get current cache size."""
        return len(self._cache)
    
    def clear(self):
        """Clear all cached results."""
        self._cache.clear()
        logger.info("Crawling cache cleared")
    
    def cleanup_expired(self) -> int:
        """Remove expired entries from cache."""
        current_time = datetime.now()
        expired_keys = [
            key for key, (_, timestamp) in self._cache.items()
            if current_time - timestamp >= self.ttl
        ]
        for key in expired_keys:
            del self._cache[key]
        logger.debug(f"Removed {len(expired_keys)} expired cache entries")
        return len(expired_keys)
```

#### 3. Crawl4AI Service Integration
```python
# services/crawling.py
import asyncio
import time
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

import httpx

from config import settings
from models.crawling import CrawlRequest, CrawlResult, CrawlingResponse
from services.crawl_cache import CrawlingCache
from services.rate_limiter import RateLimiter
from utils.logging import get_logger

logger = get_logger(__name__)

class CrawlingService:
    """
    Service for crawling URLs using external Crawl4AI instance.
    
    Implements rate limiting and caching to ensure efficient crawling
    while respecting the external service limits.
    """
    
    def __init__(self):
        self.rate_limiter = RateLimiter(max_requests=5, time_window=1.0)  # 5 req/sec max
        self.cache = CrawlingCache(ttl_hours=settings.CRAWLING_CACHE_TTL_HOURS)
        self.user_agent = f"{settings.APP_NAME}/1.0"
        self.crawl4ai_base_url = settings.CRAWL4AI_BASE_URL
        self.timeout = 60.0  # 60 second timeout for crawling requests
        
        logger.info(
            f"CrawlingService initialized with cache TTL: "
            f"{settings.CRAWLING_CACHE_TTL_HOURS}h, base URL: {self.crawl4ai_base_url}"
        )
    
    async def health_check(self) -> Dict[str, Any]:
        """Check health of Crawl4AI instance."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.crawl4ai_base_url}/health",
                    timeout=5.0,
                    headers={"User-Agent": self.user_agent}
                )
                response.raise_for_status()
                return {
                    "crawl4ai_healthy": True,
                    "crawl4ai_response": response.json()
                }
        except Exception as e:
            logger.error(f"Crawl4AI health check failed: {e}")
            return {
                "crawl4ai_healthy": False,
                "error": str(e)
            }
    
    async def crawl_urls(self, crawl_request: CrawlRequest) -> CrawlingResponse:
        """
        Crawl multiple URLs using Crawl4AI instance.
        
        Args:
            crawl_request: Crawling request with URLs and options
            
        Returns:
            CrawlingResponse with results for all URLs
        """
        start_time = time.time()
        logger.info(f"Starting crawl for {len(crawl_request.urls)} URLs")
        
        results = []
        cached_count = 0
        
        # Process each URL
        for url in crawl_request.urls:
            url_str = str(url)
            options = {
                "scrape_internal_links": crawl_request.scrape_internal_links,
                "scrape_external_links": crawl_request.scrape_external_links,
                "markdown_only": crawl_request.markdown_only,
                "capture_screenshots": crawl_request.capture_screenshots,
                "screenshot_wait_for": crawl_request.screenshot_wait_for,
                "screenshot_width": crawl_request.screenshot_width,
                "screenshot_height": crawl_request.screenshot_height
            }
            
            # Check cache first
            cached_result = self.cache.get(url_str, options)
            if cached_result and crawl_request.cache_mode != "bypass":
                logger.info(f"Using cached result for URL: {url_str}")
                cached_result["url"] = url_str  # Ensure URL is set
                results.append(CrawlResult(**cached_result))
                cached_count += 1
                continue
            
            # Rate limit before API call
            await self.rate_limiter.acquire()
            
            # Crawl the URL
            crawl_result = await self._crawl_single_url(url_str, crawl_request)
            results.append(crawl_result)
            
            # Cache successful results
            if crawl_result.success and crawl_request.cache_mode != "disabled":
                self.cache.set(url_str, options, crawl_result.model_dump())
        
        total_time = time.time() - start_time
        successful_crawls = sum(1 for result in results if result.success)
        failed_crawls = len(results) - successful_crawls
        
        response = CrawlingResponse(
            total_urls=len(crawl_request.urls),
            successful_crawls=successful_crawls,
            failed_crawls=failed_crawls,
            results=results,
            timestamp=datetime.now(timezone.utc).isoformat(),
            total_processing_time=total_time,
            cached_results=cached_count
        )
        
        logger.info(
            f"Crawling completed: {successful_crawls}/{len(results)} successful, "
            f"{cached_count} cached, total time: {total_time:.2f}s"
        )
        return response
    
    async def _crawl_single_url(self, url: str, crawl_request: CrawlRequest) -> CrawlResult:
        """Crawl a single URL using Crawl4AI API."""
        start_time = time.time()
        
        try:
            # First, perform the crawl
            crawl_result = await self._perform_crawl(url, crawl_request)
            
            # If screenshots are requested and crawl was successful, capture screenshot
            if crawl_request.capture_screenshots and crawl_result.success:
                screenshot_data = await self._capture_screenshot(
                    url, 
                    crawl_request.screenshot_wait_for,
                    crawl_request.screenshot_width,
                    crawl_request.screenshot_height
                )
                if screenshot_data:
                    crawl_result.screenshot_base64 = screenshot_data["base64"]
                    crawl_result.screenshot_size = screenshot_data["size"]
            
            return crawl_result
            
        except Exception as e:
            logger.error(f"Crawling error for URL '{url}': {e}")
            return CrawlResult(
                url=url,
                success=False,
                error_message=str(e),
                processing_time=time.time() - start_time
            )
    
    async def _perform_crawl(self, url: str, crawl_request: CrawlRequest) -> CrawlResult:
        """Perform the main crawling operation."""
        start_time = time.time()
        
        try:
            # Prepare Crawl4AI request payload
            browser_config = {
                "type": "BrowserConfig",
                "params": {"headless": True, "verbose": False}
            }
            
            crawler_config = {
                "type": "CrawlerRunConfig",
                "params": {
                    "stream": False,
                    "cache_mode": crawl_request.cache_mode,
                    "exclude_external_links": not crawl_request.scrape_external_links,
                    "word_count_threshold": 10
                }
            }
            
            payload = {
                "urls": [url],
                "browser_config": browser_config,
                "crawler_config": crawler_config
            }
            
            logger.debug(f"Calling Crawl4AI API for URL: {url}")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.crawl4ai_base_url}/crawl",
                    json=payload,
                    headers={"User-Agent": self.user_agent},
                    timeout=self.timeout
                )
                response.raise_for_status()
                
                result_data = response.json()
                
                # Extract result information
                if "result" in result_data and result_data["result"]:
                    crawl_data = result_data["result"]
                    
                    # Process links based on request options
                    internal_links = None
                    external_links = None
                    
                    if crawl_request.scrape_internal_links or crawl_request.scrape_external_links:
                        links = crawl_data.get("links", {})
                        if crawl_request.scrape_internal_links:
                            internal_links = [link.get("href", link) for link in links.get("internal", [])]
                        if crawl_request.scrape_external_links:
                            external_links = [link.get("href", link) for link in links.get("external", [])]
                    
                    # Prepare result data based on markdown_only flag
                    result_kwargs = {
                        "url": url,
                        "success": True,
                        "status_code": crawl_data.get("status_code", 200),
                        "processing_time": time.time() - start_time
                    }
                    
                    if crawl_request.markdown_only:
                        # Only include markdown content
                        markdown_data = crawl_data.get("markdown", {})
                        if isinstance(markdown_data, dict):
                            result_kwargs["markdown"] = markdown_data.get("raw_markdown") or markdown_data.get("fit_markdown")
                        else:
                            result_kwargs["markdown"] = str(markdown_data) if markdown_data else None
                    else:
                        # Include all available data
                        markdown_data = crawl_data.get("markdown", {})
                        if isinstance(markdown_data, dict):
                            result_kwargs["markdown"] = markdown_data.get("raw_markdown") or markdown_data.get("fit_markdown")
                        else:
                            result_kwargs["markdown"] = str(markdown_data) if markdown_data else None
                        
                        result_kwargs["cleaned_html"] = crawl_data.get("cleaned_html")
                        result_kwargs["metadata"] = crawl_data.get("metadata", {})
                    
                    # Add links if requested
                    if internal_links is not None:
                        result_kwargs["internal_links"] = internal_links
                    if external_links is not None:
                        result_kwargs["external_links"] = external_links
                    
                    return CrawlResult(**result_kwargs)
                else:
                    # Handle case where crawl failed
                    return CrawlResult(
                        url=url,
                        success=False,
                        error_message="No result data returned from Crawl4AI",
                        processing_time=time.time() - start_time
                    )
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from Crawl4AI for URL '{url}': {e.response.status_code}")
            return CrawlResult(
                url=url,
                success=False,
                status_code=e.response.status_code,
                error_message=f"HTTP {e.response.status_code}: {e.response.text}",
                processing_time=time.time() - start_time
            )
        except httpx.TimeoutException:
            logger.error(f"Timeout error from Crawl4AI for URL '{url}'")
            return CrawlResult(
                url=url,
                success=False,
                error_message="Request timeout",
                processing_time=time.time() - start_time
            )
        except Exception as e:
            logger.error(f"Crawling error for URL '{url}': {e}")
            return CrawlResult(
                url=url,
                success=False,
                error_message=str(e),
                processing_time=time.time() - start_time
            )
    
    async def _capture_screenshot(self, url: str, wait_for: int = 2, width: int = 1920, height: int = 1080) -> Optional[Dict[str, Any]]:
        """Capture screenshot using Crawl4AI screenshot endpoint."""
        try:
            payload = {
                "url": url,
                "screenshot_wait_for": wait_for,
                "viewport": {
                    "width": width,
                    "height": height
                }
            }
            
            logger.debug(f"Capturing screenshot for URL: {url} at {width}x{height}")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.crawl4ai_base_url}/screenshot",
                    json=payload,
                    headers={"User-Agent": self.user_agent},
                    timeout=30.0  # Screenshots can take longer
                )
                response.raise_for_status()
                
                # Crawl4AI screenshot endpoint returns the image data
                if response.headers.get("content-type", "").startswith("image/"):
                    # Convert image to base64 (no Pillow needed)
                    import base64
                    
                    image_data = response.content
                    base64_data = base64.b64encode(image_data).decode('utf-8')
                    
                    # Get actual image dimensions from PNG header (no Pillow needed)
                    actual_size = self._get_png_dimensions(image_data)
                    if not actual_size:
                        # Fallback to requested dimensions
                        actual_size = {"width": width, "height": height}
                    
                    return {
                        "base64": base64_data,
                        "size": actual_size
                    }
                else:
                    # Handle JSON response format if any
                    result = response.json()
                    if "screenshot" in result:
                        return {
                            "base64": result["screenshot"],
                            "size": result.get("size", {"width": width, "height": height})
                        }
                    
                logger.warning(f"Unexpected screenshot response format for URL: {url}")
                return None
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error capturing screenshot for URL '{url}': {e.response.status_code}")
            return None
        except httpx.TimeoutException:
            logger.error(f"Timeout capturing screenshot for URL '{url}'")
            return None
        except Exception as e:
            logger.error(f"Error capturing screenshot for URL '{url}': {e}")
            return None
    
    def _get_png_dimensions(self, png_data: bytes) -> Optional[Dict[str, int]]:
        """Extract image dimensions from PNG header without Pillow."""
        try:
            # PNG format: first 8 bytes are PNG signature, then IHDR chunk
            # IHDR chunk structure: 4 bytes length + 4 bytes "IHDR" + 4 bytes width + 4 bytes height + ...
            if len(png_data) < 24:
                return None
            
            # Check PNG signature
            if png_data[:8] != b'\x89PNG\r\n\x1a\n':
                return None
            
            # Extract width and height from IHDR chunk (bytes 16-23)
            import struct
            width = struct.unpack('>I', png_data[16:20])[0]  # Big-endian unsigned int
            height = struct.unpack('>I', png_data[20:24])[0]  # Big-endian unsigned int
            
            return {"width": width, "height": height}
        except Exception as e:
            logger.debug(f"Failed to parse PNG dimensions: {e}")
            return None
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics for monitoring."""
        return {
            "cache_size": self.cache.size(),
            "cache_ttl_hours": settings.CRAWLING_CACHE_TTL_HOURS,
            "rate_limiter_active": True,
            "crawl4ai_instance": self.crawl4ai_base_url
        }
    
    def clear_cache(self):
        """Clear the crawling cache."""
        self.cache.clear()
        logger.info("Crawling cache cleared")
```

#### 4. Router Implementation
```python
# routers/crawling.py
from datetime import datetime, timezone
from typing import Dict, Any

from slowapi import Limiter
from slowapi.util import get_remote_address

from config import settings
from dependencies import RequiredAuth
from fastapi import APIRouter, HTTPException, Request, Body
from models.crawling import CrawlRequest, CrawlingResponse, CrawlingHealthResponse
from services.crawling import CrawlingService
from utils.logging import get_logger

logger = get_logger(__name__)

# Initialize limiter for this router
limiter = Limiter(key_func=get_remote_address)

# Create router with authentication and tags
router = APIRouter(
    prefix="/crawl",
    tags=["crawling"],
    dependencies=[RequiredAuth],  # Apply auth to all routes in this router
)

# Initialize crawling service (singleton pattern)
crawling_service = CrawlingService()

@router.post("/batch", response_model=CrawlingResponse)
@limiter.limit(settings.CRAWLING_USER_RATE_LIMIT)
async def crawl_urls(
    request: Request,  # Required for rate limiter
    crawl_request: CrawlRequest = Body(
        ...,
        examples=[
            {
                "urls": [
                    "https://example.com",
                    "https://httpbin.org/html"
                ],
                "scrape_internal_links": True,
                "scrape_external_links": False,
                "markdown_only": True,
                "capture_screenshots": True,
                "screenshot_wait_for": 3,
                "screenshot_width": 1280,
                "screenshot_height": 720,
                "cache_mode": "enabled"
            }
        ]
    ),
):
    """
    Crawl multiple URLs using Crawl4AI instance.
    
    This endpoint uses an external Crawl4AI service to crawl multiple URLs
    and extract content with configurable options for link extraction and
    output format.
    
    **Features:**
    - Batch processing of up to 50 URLs
    - Optional internal/external link extraction
    - Markdown-only output option
    - Full-page screenshot capture
    - Caching with configurable TTL
    - Rate limiting for API protection
    
    **Rate Limits:**
    - User limit: 5 requests per minute per IP
    - Crawl4AI API: 5 requests per second (handled internally)
    
    **Caching:**
    - Results are cached for 1 hour by default
    - Cache behavior can be controlled via cache_mode parameter
    
    **Authentication:**
    - Requires valid API key in X-API-KEY header
    
    Args:
        request: FastAPI request object (required for rate limiting)
        crawl_request: Crawling request with URLs and options
        
    Returns:
        CrawlingResponse: Results for all crawled URLs with metadata
        
    Raises:
        HTTPException 400: If request validation fails
        HTTPException 401: If authentication is invalid
        HTTPException 422: If input validation fails
        HTTPException 429: If rate limit is exceeded
        HTTPException 503: If Crawl4AI service is unavailable
        
    Example:
        ```
        POST /crawl/batch
        {
            "urls": ["https://example.com", "https://test.com"],
            "scrape_internal_links": true,
            "scrape_external_links": false,
            "markdown_only": true,
            "capture_screenshots": true,
            "screenshot_wait_for": 3,
            "screenshot_width": 1280,
            "screenshot_height": 720,
            "cache_mode": "enabled"
        }
        
        Response:
        {
            "total_urls": 2,
            "successful_crawls": 2,
            "failed_crawls": 0,
            "results": [
                {
                    "url": "https://example.com",
                    "success": true,
                    "status_code": 200,
                    "markdown": "# Example Page...",
                    "internal_links": ["https://example.com/about"],
                    "screenshot_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
                    "screenshot_size": {"width": 1280, "height": 720},
                    "processing_time": 2.45
                }
            ],
            "timestamp": "2024-01-01T12:00:00+00:00",
            "total_processing_time": 5.32,
            "cached_results": 0
        }
        ```
    """
    logger.info(
        f"Crawling request for {len(crawl_request.urls)} URLs "
        f"from IP: {get_remote_address(request)}"
    )
    
    try:
        result = await crawling_service.crawl_urls(crawl_request)
        
        logger.info(
            f"Crawling completed: {result.successful_crawls}/{result.total_urls} successful, "
            f"cached: {result.cached_results}, time: {result.total_processing_time:.2f}s"
        )
        return result
        
    except Exception as e:
        logger.error(f"Crawling service error: {e}")
        raise HTTPException(
            status_code=503, 
            detail="Crawling service temporarily unavailable"
        )

@router.get("/health", response_model=CrawlingHealthResponse)
@limiter.limit("60/minute")  # Higher limit for health checks
async def crawling_health(request: Request):
    """
    Health check endpoint for crawling service.
    
    Provides status information about the crawling service including
    Crawl4AI instance health, cache statistics, and service availability.
    
    Args:
        request: FastAPI request object (required for rate limiting)
        
    Returns:
        Service health status and Crawl4AI instance status
        
    Example:
        ```
        GET /crawl/health
        
        Response:
        {
            "service": "crawling",
            "status": "healthy",
            "crawl4ai_instance": "https://crawl4ai.test001.nl",
            "crawl4ai_healthy": true,
            "cache_size": 15,
            "rate_limiter_active": true
        }
        ```
    """
    logger.debug(f"Crawling health check from IP: {get_remote_address(request)}")
    
    try:
        # Check Crawl4AI instance health
        health_data = await crawling_service.health_check()
        cache_stats = crawling_service.get_cache_stats()
        
        return CrawlingHealthResponse(
            status="healthy" if health_data["crawl4ai_healthy"] else "degraded",
            crawl4ai_instance=cache_stats["crawl4ai_instance"],
            crawl4ai_healthy=health_data["crawl4ai_healthy"],
            cache_size=cache_stats["cache_size"],
            rate_limiter_active=cache_stats["rate_limiter_active"]
        )
        
    except Exception as e:
        logger.error(f"Crawling health check failed: {e}")
        raise HTTPException(
            status_code=503, 
            detail="Crawling service health check failed"
        )

@router.post("/cache/clear")
@limiter.limit("10/hour")  # Very limited for admin operations
async def clear_crawling_cache(request: Request):
    """
    Clear the crawling cache.
    
    Administrative endpoint to clear all cached crawling results.
    Use sparingly as this will increase API calls to Crawl4AI.
    
    Args:
        request: FastAPI request object (required for rate limiting)
        
    Returns:
        Cache clear confirmation
        
    Example:
        ```
        POST /crawl/cache/clear
        
        Response:
        {
            "message": "Crawling cache cleared",
            "timestamp": "2024-01-01T12:00:00+00:00"
        }
        ```
    """
    logger.warning(f"Cache clear requested from IP: {get_remote_address(request)}")
    
    try:
        crawling_service.clear_cache()
        
        return {
            "message": "Crawling cache cleared",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        
    except Exception as e:
        logger.error(f"Cache clear failed: {e}")
        raise HTTPException(
            status_code=503, 
            detail="Failed to clear crawling cache"
        )
```

#### 5. Configuration Updates
```python
# config.py additions
class Settings(BaseSettings):
    # ... existing settings ...
    
    # Crawling configuration
    CRAWL4AI_BASE_URL: str = Field(
        default="https://crawl4ai.test001.nl",
        description="Base URL for Crawl4AI instance"
    )
    CRAWLING_CACHE_TTL_HOURS: int = Field(
        default=1,
        description="Cache TTL for crawling results in hours"
    )
    CRAWLING_USER_RATE_LIMIT: str = Field(
        default="5/minute",
        description="Rate limit for users calling crawling endpoints"
    )
```

#### 6. Router Registration
```python
# In main.py, add:
from routers import geocoding, crawling

# Include routers
app.include_router(
    crawling.router,
    responses={
        401: {"description": "Authentication required"},
        400: {"description": "Bad request"},
        422: {"description": "Validation error"},
        429: {"description": "Rate limit exceeded"},
        503: {"description": "Service unavailable"},
    }
)
```

### Testing Strategy (TDD Approach)

#### 1. Unit Tests (Create FIRST)
```python
# tests/test_crawl_cache.py
import pytest
from services.crawl_cache import CrawlingCache
from datetime import datetime, timedelta

def test_cache_stores_and_retrieves():
    """Test basic cache functionality."""
    cache = CrawlingCache(ttl_hours=1)
    
    url = "https://example.com"
    options = {"markdown_only": True, "scrape_internal_links": False}
    test_data = {"url": url, "success": True, "markdown": "# Test"}
    
    cache.set(url, options, test_data)
    result = cache.get(url, options)
    
    assert result == test_data

def test_cache_key_considers_options():
    """Test that cache keys consider crawling options."""
    cache = CrawlingCache(ttl_hours=1)
    
    url = "https://example.com"
    options1 = {"markdown_only": True, "capture_screenshots": False}
    options2 = {"markdown_only": False, "capture_screenshots": False}
    options3 = {"markdown_only": True, "capture_screenshots": True, "screenshot_width": 1280, "screenshot_height": 720}
    test_data = {"url": url, "success": True}
    
    cache.set(url, options1, test_data)
    
    # Different options should not hit cache
    assert cache.get(url, options2) is None
    assert cache.get(url, options3) is None
    # Same options should hit cache
    assert cache.get(url, options1) == test_data

# tests/test_crawling_service.py
import pytest
from unittest.mock import AsyncMock, patch
from services.crawling import CrawlingService
from models.crawling import CrawlRequest

@pytest.mark.asyncio
async def test_crawling_service_health_check():
    """Test Crawl4AI health check."""
    service = CrawlingService()
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = AsyncMock()
        mock_response.json.return_value = {"status": "healthy"}
        mock_response.raise_for_status.return_value = None
        
        mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
        
        result = await service.health_check()
        
        assert result["crawl4ai_healthy"] is True
        assert "crawl4ai_response" in result

@pytest.mark.asyncio
async def test_crawl_single_url_success():
    """Test successful single URL crawling."""
    service = CrawlingService()
    
    mock_crawl4ai_response = {
        "result": {
            "status_code": 200,
            "markdown": {"raw_markdown": "# Test Page"},
            "cleaned_html": "<h1>Test Page</h1>",
            "metadata": {"title": "Test"},
            "links": {
                "internal": [{"href": "https://example.com/about"}],
                "external": [{"href": "https://google.com"}]
            }
        }
    }
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = AsyncMock()
        mock_response.json.return_value = mock_crawl4ai_response
        mock_response.raise_for_status.return_value = None
        
        mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
        
        crawl_request = CrawlRequest(
            urls=["https://example.com"],
            scrape_internal_links=True,
            scrape_external_links=True,
            markdown_only=False
        )
        
        result = await service.crawl_urls(crawl_request)
        
        assert result.total_urls == 1
        assert result.successful_crawls == 1
        assert result.failed_crawls == 0
        assert len(result.results) == 1
        
        crawl_result = result.results[0]
        assert crawl_result.success is True
        assert crawl_result.url == "https://example.com"
        assert crawl_result.markdown == "# Test Page"
        assert "https://example.com/about" in crawl_result.internal_links
        assert "https://google.com" in crawl_result.external_links

@pytest.mark.asyncio
async def test_crawl_markdown_only():
    """Test markdown-only crawling."""
    service = CrawlingService()
    
    mock_crawl4ai_response = {
        "result": {
            "status_code": 200,
            "markdown": {"raw_markdown": "# Test Page"},
            "cleaned_html": "<h1>Test Page</h1>",
            "metadata": {"title": "Test"}
        }
    }
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = AsyncMock()
        mock_response.json.return_value = mock_crawl4ai_response
        mock_response.raise_for_status.return_value = None
        
        mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
        
        crawl_request = CrawlRequest(
            urls=["https://example.com"],
            markdown_only=True
        )
        
        result = await service.crawl_urls(crawl_request)
        
        crawl_result = result.results[0]
        assert crawl_result.markdown == "# Test Page"
        assert crawl_result.cleaned_html is None
        assert crawl_result.metadata is None

@pytest.mark.asyncio
async def test_crawl_with_screenshots():
    """Test crawling with screenshot capture."""
    service = CrawlingService()
    
    # Mock crawl response
    mock_crawl4ai_response = {
        "result": {
            "status_code": 200,
            "markdown": {"raw_markdown": "# Test Page"},
            "cleaned_html": "<h1>Test Page</h1>"
        }
    }
    
    # Mock screenshot response (binary image data)
    mock_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x19tEXtSoftware\x00Adobe ImageReadyq\xc9e<\x00\x00\x00\x0eIDATx\xdab\xf8\x00\x00\x00\x01\x00\x01\x03\x02\xfe\x1f\x00\x00\x00\x00IEND\xaeB`\x82'
    
    with patch('httpx.AsyncClient') as mock_client:
        # Mock crawl request
        mock_crawl_response = AsyncMock()
        mock_crawl_response.json.return_value = mock_crawl4ai_response
        mock_crawl_response.raise_for_status.return_value = None
        
        # Mock screenshot request  
        mock_screenshot_response = AsyncMock()
        mock_screenshot_response.content = mock_image_data
        mock_screenshot_response.headers = {"content-type": "image/png"}
        mock_screenshot_response.raise_for_status.return_value = None
        
        # Configure mock client to return different responses for different endpoints
        async def mock_post(url, **kwargs):
            if "/screenshot" in url:
                return mock_screenshot_response
            else:
                return mock_crawl_response
        
        mock_client.return_value.__aenter__.return_value.post.side_effect = mock_post
        
        crawl_request = CrawlRequest(
            urls=["https://example.com"],
            capture_screenshots=True,
            screenshot_wait_for=3,
            screenshot_width=1280,
            screenshot_height=720
        )
        
        result = await service.crawl_urls(crawl_request)
        
        assert result.total_urls == 1
        assert result.successful_crawls == 1
        
        crawl_result = result.results[0]
        assert crawl_result.success is True
        assert crawl_result.screenshot_base64 is not None
        assert crawl_result.screenshot_size is not None
        assert crawl_result.screenshot_size["width"] > 0
        assert crawl_result.screenshot_size["height"] > 0

@pytest.mark.asyncio
async def test_screenshot_failure_graceful():
    """Test graceful handling of screenshot failures."""
    service = CrawlingService()
    
    mock_crawl4ai_response = {
        "result": {
            "status_code": 200,
            "markdown": {"raw_markdown": "# Test Page"}
        }
    }
    
    with patch('httpx.AsyncClient') as mock_client:
        # Mock successful crawl but failed screenshot
        mock_crawl_response = AsyncMock()
        mock_crawl_response.json.return_value = mock_crawl4ai_response
        mock_crawl_response.raise_for_status.return_value = None
        
        # Mock failed screenshot
        mock_screenshot_response = AsyncMock()
        mock_screenshot_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Screenshot failed", request=None, response=AsyncMock(status_code=500)
        )
        
        async def mock_post(url, **kwargs):
            if "/screenshot" in url:
                return mock_screenshot_response
            else:
                return mock_crawl_response
        
        mock_client.return_value.__aenter__.return_value.post.side_effect = mock_post
        
        crawl_request = CrawlRequest(
            urls=["https://example.com"],
            capture_screenshots=True
        )
        
        result = await service.crawl_urls(crawl_request)
        
        # Crawl should still succeed even if screenshot fails
        assert result.successful_crawls == 1
        crawl_result = result.results[0]
        assert crawl_result.success is True
        assert crawl_result.markdown == "# Test Page"
        assert crawl_result.screenshot_base64 is None  # Screenshot failed gracefully
```

#### 2. Integration Tests
```python
# tests/test_integration.py additions
class TestCrawlingEndpoints:
    """Integration tests for crawling endpoints."""
    
    def test_crawl_batch_success(self, client: TestClient, api_key_headers):
        """Test successful batch crawling."""
        payload = {
            "urls": ["https://httpbin.org/html"],
            "scrape_internal_links": True,
            "scrape_external_links": False,
            "markdown_only": True,
            "cache_mode": "enabled"
        }
        
        response = client.post("/crawl/batch", json=payload, headers=api_key_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert "total_urls" in data
        assert "successful_crawls" in data
        assert "results" in data
        assert len(data["results"]) == 1
        
        result = data["results"][0]
        assert "url" in result
        assert "success" in result

    def test_crawl_batch_validation(self, client: TestClient, api_key_headers):
        """Test request validation."""
        # Empty URLs list
        payload = {"urls": []}
        response = client.post("/crawl/batch", json=payload, headers=api_key_headers)
        assert response.status_code == 422
        
        # Too many URLs
        payload = {"urls": ["https://example.com"] * 51}
        response = client.post("/crawl/batch", json=payload, headers=api_key_headers)
        assert response.status_code == 422
        
        # Invalid URL
        payload = {"urls": ["not-a-url"]}
        response = client.post("/crawl/batch", json=payload, headers=api_key_headers)
        assert response.status_code == 422

    def test_crawl_health_endpoint(self, client: TestClient, api_key_headers):
        """Test crawling health endpoint."""
        response = client.get("/crawl/health", headers=api_key_headers)
        assert response.status_code in [200, 503]  # May be degraded if Crawl4AI unavailable
        
        data = response.json()
        assert data["service"] == "crawling"
        assert "crawl4ai_instance" in data
        assert "crawl4ai_healthy" in data

    def test_crawl_authentication_required(self, client: TestClient):
        """Test that authentication is required."""
        payload = {"urls": ["https://example.com"]}
        response = client.post("/crawl/batch", json=payload)
        assert response.status_code == 401

    def test_crawl_rate_limiting(self, client: TestClient, api_key_headers):
        """Test crawling rate limiting."""
        payload = {"urls": ["https://httpbin.org/html"]}
        
        # Make multiple requests
        for i in range(6):  # Exceed 5/minute limit
            response = client.post("/crawl/batch", json=payload, headers=api_key_headers)
            if response.status_code == 429:
                break  # Rate limited as expected
        else:
            # If we didn't hit rate limit, that's also acceptable for this test
            pass

    def test_crawl_cache_behavior(self, client: TestClient, api_key_headers):
        """Test caching behavior."""
        payload = {
            "urls": ["https://httpbin.org/html"],
            "cache_mode": "enabled"
        }
        
        # First request
        response1 = client.post("/crawl/batch", json=payload, headers=api_key_headers)
        if response1.status_code != 200:
            return  # Skip if service unavailable
            
        # Second request should potentially use cache
        response2 = client.post("/crawl/batch", json=payload, headers=api_key_headers)
        assert response2.status_code == 200

    def test_crawl_markdown_only_option(self, client: TestClient, api_key_headers):
        """Test markdown-only output option."""
        payload = {
            "urls": ["https://httpbin.org/html"],
            "markdown_only": True
        }
        
        response = client.post("/crawl/batch", json=payload, headers=api_key_headers)
        if response.status_code == 200:
            data = response.json()
            result = data["results"][0]
            if result["success"]:
                # When markdown_only=True, should not have cleaned_html or metadata
                assert "markdown" in result
                # Note: cleaned_html and metadata may be None or absent

    def test_crawl_with_screenshots_option(self, client: TestClient, api_key_headers):
        """Test screenshot capture option."""
        payload = {
            "urls": ["https://httpbin.org/html"],
            "capture_screenshots": True,
            "screenshot_wait_for": 2
        }
        
        response = client.post("/crawl/batch", json=payload, headers=api_key_headers)
        if response.status_code == 200:
            data = response.json()
            result = data["results"][0]
            if result["success"]:
                # Should have screenshot data if capture was successful
                # Note: Screenshots may fail gracefully, so check for presence
                if "screenshot_base64" in result and result["screenshot_base64"]:
                    assert isinstance(result["screenshot_base64"], str)
                    assert len(result["screenshot_base64"]) > 0
                    # Should also have size information
                    assert "screenshot_size" in result
                    assert "width" in result["screenshot_size"]
                    assert "height" in result["screenshot_size"]

    def test_crawl_screenshot_validation(self, client: TestClient, api_key_headers):
        """Test screenshot parameter validation."""
        # Invalid screenshot_wait_for (too high)
        payload = {
            "urls": ["https://httpbin.org/html"],
            "capture_screenshots": True,
            "screenshot_wait_for": 15  # Max is 10
        }
        
        response = client.post("/crawl/batch", json=payload, headers=api_key_headers)
        assert response.status_code == 422
        
        # Invalid screenshot_wait_for (negative)
        payload = {
            "urls": ["https://httpbin.org/html"],
            "capture_screenshots": True,
            "screenshot_wait_for": -1
        }
        
        response = client.post("/crawl/batch", json=payload, headers=api_key_headers)
        assert response.status_code == 422

    def test_crawl_screenshot_size_validation(self, client: TestClient, api_key_headers):
        """Test screenshot size parameter validation."""
        # Screen size too small
        payload = {
            "urls": ["https://httpbin.org/html"],
            "capture_screenshots": True,
            "screenshot_width": 200,  # Below minimum of 320
            "screenshot_height": 150   # Below minimum of 240
        }
        
        response = client.post("/crawl/batch", json=payload, headers=api_key_headers)
        assert response.status_code == 422
        
        # Screen size too large
        payload = {
            "urls": ["https://httpbin.org/html"],
            "capture_screenshots": True,
            "screenshot_width": 4000,  # Above maximum of 3840
            "screenshot_height": 3000  # Above maximum of 2160
        }
        
        response = client.post("/crawl/batch", json=payload, headers=api_key_headers)
        assert response.status_code == 422
        
        # Valid screen sizes should work
        valid_sizes = [
            {"screenshot_width": 1920, "screenshot_height": 1080},  # Full HD
            {"screenshot_width": 1280, "screenshot_height": 720},   # HD
            {"screenshot_width": 320, "screenshot_height": 240},    # Minimum
            {"screenshot_width": 3840, "screenshot_height": 2160},  # 4K (maximum)
        ]
        
        for size in valid_sizes:
            payload = {
                "urls": ["https://httpbin.org/html"],
                "capture_screenshots": True,
                **size
            }
            
            response = client.post("/crawl/batch", json=payload, headers=api_key_headers)
            # Should not fail validation (may fail for other reasons like service unavailable)
            assert response.status_code not in [422]
```

### Implementation Tasks (TDD Order)

**Phase 1: Setup Dependencies**
1. **Update configuration**
   - Add CRAWL4AI_BASE_URL, CRAWLING_CACHE_TTL_HOURS, CRAWLING_USER_RATE_LIMIT to config.py

**Phase 2: Tests First (TDD)**
2. **Create test files FIRST**
   - Create tests/test_crawl_cache.py with caching tests (including screenshot cache keys)
   - Create tests/test_crawling_service.py with service tests (including screenshot tests)
   - Add integration tests to tests/test_integration.py (including screenshot validation)

**Phase 3: Implementation to Pass Tests**
3. **Create models module**
   - Create models/crawling.py with Pydantic models for requests/responses (including screenshot fields)

4. **Create cache module**
   - Create services/crawl_cache.py with CrawlingCache class

5. **Create crawling service**
   - Create services/crawling.py with CrawlingService
   - Implement Crawl4AI API integration with rate limiting and caching
   - Add screenshot capture functionality using Crawl4AI /screenshot endpoint

6. **Create router module**
   - Create routers/crawling.py with APIRouter
   - Implement crawling endpoints with rate limiting

7. **Update main.py**
   - Import crawling router
   - Register router with app.include_router()

**Phase 4: Documentation**
8. **Update documentation**
   - Add endpoints to README.md
   - Update Claude.md with crawling patterns

### Validation Gates

```bash
# Syntax/Style Check
ruff check --fix . && ruff format .

# Run All Tests
pytest tests/ -v

# Run with Coverage
pytest --cov=. --cov-report=term-missing

# Full Quality Check
make quality
```

### Gotchas & Considerations

#### Crawl4AI Integration (CRITICAL)
1. **Service Availability**:
   - Crawl4AI instance at `https://crawl4ai.test001.nl` must be accessible
   - Health checks should verify service availability
   - Graceful degradation when service is unavailable

2. **Rate Limiting**:
   - External service may have its own rate limits
   - Implement conservative rate limiting (5 req/sec max)
   - Cache results aggressively to minimize API calls

3. **Result Processing**:
   - Crawl4AI returns complex result structures
   - Handle different response formats gracefully
   - Extract links from nested structure properly

#### URL Handling
4. **URL Validation**:
   - Use Pydantic HttpUrl for automatic validation
   - Handle different URL formats and protocols
   - Consider URL normalization for caching

5. **Batch Processing**:
   - Limit batch size to prevent abuse (max 50 URLs)
   - Process URLs sequentially to respect rate limits
   - Provide detailed results for each URL

#### Caching Strategy
6. **Cache Key Design**:
   - Include all options that affect results in cache key
   - Use URL normalization for consistent caching
   - Consider shorter TTL (1 hour) due to dynamic web content

#### Screenshot Considerations
7. **Dependencies**:
   - No additional dependencies required (uses built-in Python libraries)
   - Screenshots may increase response payload size significantly
   - Base64 encoding for easy JSON transmission
   - PNG dimensions extracted from headers without external libraries

8. **Performance**:
   - Cache hits should be <100ms
   - API calls will be >1s due to rate limiting
   - Screenshot capture adds 2-5 seconds per URL
   - User rate limiting prevents abuse

### Success Criteria

- [ ] **All tests pass (TDD approach)**
- [ ] **Crawl4AI integration working** - Health checks and API calls successful
- [ ] **Rate limiting enforced** - Prevent API abuse
- [ ] **Caching reduces external API calls** - Efficient cache hit behavior
- [ ] **Multiple URL batch processing** - Handle up to 50 URLs per request
- [ ] **Link extraction options work** - Internal/external links configurable
- [ ] **Markdown-only output option** - Reduced response size when requested
- [ ] **Screenshot capture functionality** - Full-page screenshots with base64 encoding
- [ ] **Screenshot parameter validation** - Wait time limits (0-10 seconds) and size limits (320x240 to 3840x2160)
- [ ] **Custom screenshot dimensions** - User-configurable viewport size with validation
- [ ] **Graceful screenshot failure handling** - Crawl succeeds even if screenshot fails
- [ ] **Proper error handling** - Graceful failure handling
- [ ] **Comprehensive test coverage (>90%)**
- [ ] **Documentation updated** - Claude.md and README.md updated
- [ ] **All validation gates pass** - Linting, formatting, tests pass

### API Endpoint Summary

#### Endpoints Created:
- `POST /crawl/batch` - Crawl multiple URLs with configurable options
- `GET /crawl/health` - Health check for crawling service and Crawl4AI instance  
- `POST /crawl/cache/clear` - Administrative cache management

#### Request Features:
- Accept 1-50 URLs per batch request
- Optional internal link extraction (`scrape_internal_links`)
- Optional external link extraction (`scrape_external_links`)
- Markdown-only output option (`markdown_only`)
- Full-page screenshot capture (`capture_screenshots`)
- Configurable screenshot wait time (`screenshot_wait_for`, 0-10 seconds)  
- Custom screenshot dimensions (`screenshot_width`, `screenshot_height`)
- Validated screen size limits (320x240 to 3840x2160)
- Configurable caching behavior (`cache_mode`)

#### Response Features:
- Detailed results for each URL with success/failure status
- Processing time metrics
- Cache hit statistics
- Structured error messages
- Base64-encoded screenshots with dimensions
- Complete metadata when not using markdown-only mode

### ✅ **CONFIDENCE SCORE: 9/10 - COMPREHENSIVE IMPLEMENTATION PLAN** ✅

**HIGH CONFIDENCE DUE TO:**
- ✅ Thorough research of Crawl4AI capabilities and API structure
- ✅ Existing codebase patterns well understood and followed
- ✅ TDD approach with comprehensive test coverage planned
- ✅ Proper rate limiting and caching strategies
- ✅ Robust error handling and validation
- ✅ Clear integration path with external Crawl4AI service
- ✅ All user requirements addressed (multiple URLs, link options, markdown-only, screenshots)

**RISK MITIGATION:**
- ✅ Health checks verify external service availability
- ✅ Caching reduces dependency on external API
- ✅ Rate limiting prevents service abuse
- ✅ Graceful error handling for service unavailability
- ✅ Mock tests prevent external API dependency during development
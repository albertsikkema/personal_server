"""
Crawling service with Crawl4AI integration.

This module provides web crawling functionality using the Crawl4AI service,
including screenshot capture, link extraction, and caching.
"""

import asyncio
import base64
import struct
import time
from typing import Any
from urllib.parse import urljoin, urlparse, urlunparse

import httpx

from config import settings
from models.crawling import (
    CacheClearResponse,
    CrawlRequest,
    CrawlResult,
    CrawlingHealthResponse,
    CrawlingResponse,
)
from services.crawl_cache import CrawlingCache
from services.rate_limiter import RateLimiter


class CrawlingService:
    """
    Service for crawling web pages using Crawl4AI.

    Provides rate limiting, caching, screenshot capture, and link extraction.
    """

    def __init__(self):
        """Initialize the crawling service."""
        # Rate limiter for Crawl4AI API (1 request per second for safety)
        self.rate_limiter = RateLimiter(max_requests=1, time_window=1.0)

        # Cache for crawling results
        self.cache = CrawlingCache(ttl_hours=settings.CRAWLING_CACHE_TTL_HOURS)

        # Crawl4AI configuration
        self.base_url = settings.CRAWL4AI_BASE_URL.rstrip("/")
        self.user_agent = f"{settings.APP_NAME}/1.0"
        self.api_token = settings.CRAWL4AI_API_TOKEN

        # HTTP timeout settings
        self.timeout = httpx.Timeout(30.0, connect=10.0)

    def _build_headers(self, content_type: str | None = None) -> dict[str, str]:
        """
        Build HTTP headers for Crawl4AI requests.

        Args:
            content_type: Optional content type header

        Returns:
            Dictionary of headers
        """
        headers = {"User-Agent": self.user_agent}

        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"

        if content_type:
            headers["Content-Type"] = content_type

        return headers

    async def _wait_for_task_completion(
        self, client: httpx.AsyncClient, task_id: str
    ) -> dict[str, Any]:
        """
        Wait for Crawl4AI task to complete and return results.

        Args:
            client: HTTP client instance
            task_id: Task ID from Crawl4AI

        Returns:
            Task results when completed

        Raises:
            httpx.HTTPError: If task fails or times out
        """
        max_polls = 30  # 30 seconds max wait
        poll_interval = 1.0  # 1 second between polls

        for _attempt in range(max_polls):
            await asyncio.sleep(poll_interval)

            response = await client.get(
                f"{self.base_url}/task/{task_id}", headers=self._build_headers()
            )
            response.raise_for_status()

            task_result = response.json()
            status = task_result.get("status")

            if status == "completed":
                return task_result
            elif status == "failed":
                raise httpx.HTTPError(
                    f"Crawl task failed: {task_result.get('error', 'Unknown error')}"
                )
            elif status in ["pending", "running", "processing"]:
                continue  # Keep polling
            else:
                raise httpx.HTTPError(f"Unknown task status: {status}")

        raise httpx.HTTPError(f"Task {task_id} timed out after {max_polls} seconds")

    async def health_check(self) -> dict[str, Any]:
        """
        Check health of the crawling service and Crawl4AI instance.

        Returns:
            Health status dictionary
        """
        health_data = {
            "crawl4ai_healthy": False,
            "error": None,
            "crawl4ai_response": None,
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/health", headers=self._build_headers()
                )
                response.raise_for_status()

                crawl4ai_data = response.json()
                health_data["crawl4ai_healthy"] = True
                health_data["crawl4ai_response"] = crawl4ai_data

        except Exception as e:
            health_data["error"] = str(e)

        return health_data

    async def crawl_urls(self, request: CrawlRequest) -> CrawlingResponse:
        """
        Crawl multiple URLs according to the request configuration.

        Supports recursive crawling when follow_internal_links is enabled.

        Args:
            request: Crawling request with URLs and options

        Returns:
            CrawlingResponse with results for all URLs
        """
        start_time = time.time()

        if request.follow_internal_links or request.follow_external_links:
            # Use recursive crawling logic
            results, cached_count = await self._crawl_recursive(request)
        else:
            # Use simple crawling logic
            results, cached_count = await self._crawl_simple(request)

        total_time = time.time() - start_time

        return CrawlingResponse.create_from_results(
            results=results, cached_count=cached_count, total_time=total_time
        )

    async def _crawl_simple(
        self, request: CrawlRequest
    ) -> tuple[list[CrawlResult], int]:
        """
        Simple crawling without following links.

        Args:
            request: Crawling request

        Returns:
            Tuple of (results list, cached count)
        """
        results = []
        cached_count = 0

        # Convert crawl request to options dictionary for caching
        options = self._request_to_options(request)

        for url in request.urls:
            url_str = str(url)

            # Check cache first (unless bypassing)
            if request.cache_mode != "bypass":
                cached_result = self.cache.get(url_str, options)
                if cached_result:
                    cached_count += 1
                    results.append(CrawlResult(**cached_result))
                    continue

            # Crawl the URL
            result = await self._crawl_single_url(url_str, request, depth=0)
            results.append(result)

            # Cache successful results (unless disabled)
            if request.cache_mode != "disabled" and result.success:
                self.cache.set(url_str, options, result.model_dump())

        return results, cached_count

    def _normalize_url(self, url: str) -> str:
        """
        Normalize URL for deduplication.

        Removes fragments (#), trailing slashes, and converts to lowercase domain.

        Args:
            url: Raw URL to normalize

        Returns:
            Normalized URL string
        """
        parsed = urlparse(url)

        # Normalize path: remove trailing slash except for root path
        path = parsed.path
        normalized_path = "" if path == "" or path == "/" else path.rstrip("/")

        # Remove fragment (everything after #)
        normalized = urlunparse(
            (
                parsed.scheme.lower(),  # Lowercase scheme
                parsed.netloc.lower(),  # Lowercase domain
                normalized_path,  # Normalized path
                parsed.params,
                parsed.query,
                "",  # Remove fragment
            )
        )

        return normalized

    async def _crawl_recursive(
        self, request: CrawlRequest
    ) -> tuple[list[CrawlResult], int]:
        """
        Recursive crawling following internal and/or external links up to max_depth.

        Ensures each normalized URL is only crawled once, including handling
        fragments (#) and other URL variations.

        Args:
            request: Crawling request with follow_internal_links or follow_external_links enabled

        Returns:
            Tuple of (results list, cached count)
        """
        results = []
        cached_count = 0
        crawled_urls = set()  # Track normalized URLs to prevent duplicates
        to_crawl = []

        # Convert crawl request to options dictionary for caching
        options = self._request_to_options(request)

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

            # Check cache first (unless bypassing)
            if request.cache_mode != "bypass":
                cached_result = self.cache.get(url_str, options)
                if cached_result:
                    cached_count += 1
                    # Update depth in cached result
                    cached_result["depth"] = depth
                    results.append(CrawlResult(**cached_result))

                    # If we can go deeper, add discovered links to queue
                    if (
                        depth < request.max_depth - 1
                        and len(results) < request.max_pages
                    ):
                        # Add internal links if following internal links
                        if request.follow_internal_links and cached_result.get(
                            "internal_links"
                        ):
                            for link in cached_result["internal_links"]:
                                absolute_url = urljoin(url_str, link)
                                normalized_link = self._normalize_url(absolute_url)
                                # Skip if already crawled
                                if normalized_link in crawled_urls:
                                    continue
                                # Only follow links from the same domain
                                parsed_link = urlparse(absolute_url)
                                if parsed_link.netloc == urlparse(base_domain).netloc:
                                    to_crawl.append(
                                        (
                                            absolute_url,
                                            normalized_link,
                                            depth + 1,
                                            base_domain,
                                        )
                                    )

                        # Add external links if following external links
                        if request.follow_external_links and cached_result.get(
                            "external_links"
                        ):
                            for link in cached_result["external_links"]:
                                # External links are already absolute URLs
                                normalized_link = self._normalize_url(link)
                                # Skip if already crawled
                                if normalized_link in crawled_urls:
                                    continue
                                parsed_link = urlparse(link)
                                if parsed_link.netloc != urlparse(base_domain).netloc:
                                    # Use the external domain as the new base for future links
                                    external_domain = (
                                        f"{parsed_link.scheme}://{parsed_link.netloc}"
                                    )
                                    to_crawl.append(
                                        (
                                            link,
                                            normalized_link,
                                            depth + 1,
                                            external_domain,
                                        )
                                    )
                    continue

            # Crawl the URL
            result = await self._crawl_single_url(url_str, request, depth=depth)
            results.append(result)

            # Cache successful results (unless disabled)
            if request.cache_mode != "disabled" and result.success:
                self.cache.set(url_str, options, result.model_dump())

            # If successful and we can go deeper, add discovered links to queue
            if (
                result.success
                and depth < request.max_depth - 1
                and len(results) < request.max_pages
            ):
                # Add internal links if following internal links
                if request.follow_internal_links and result.internal_links:
                    for link in result.internal_links:
                        absolute_url = urljoin(url_str, link)
                        normalized_link = self._normalize_url(absolute_url)
                        # Skip if already crawled
                        if normalized_link in crawled_urls:
                            continue
                        # Only follow links from the same domain
                        parsed_link = urlparse(absolute_url)
                        if parsed_link.netloc == urlparse(base_domain).netloc:
                            to_crawl.append(
                                (absolute_url, normalized_link, depth + 1, base_domain)
                            )

                # Add external links if following external links
                if request.follow_external_links and result.external_links:
                    for link in result.external_links:
                        # External links are already absolute URLs
                        normalized_link = self._normalize_url(link)
                        # Skip if already crawled
                        if normalized_link in crawled_urls:
                            continue
                        parsed_link = urlparse(link)
                        if parsed_link.netloc != urlparse(base_domain).netloc:
                            # Use the external domain as the new base for future links
                            external_domain = (
                                f"{parsed_link.scheme}://{parsed_link.netloc}"
                            )
                            to_crawl.append(
                                (link, normalized_link, depth + 1, external_domain)
                            )

        return results, cached_count

    async def _crawl_single_url(
        self, url: str, request: CrawlRequest, depth: int = 0
    ) -> CrawlResult:
        """
        Crawl a single URL with the specified options.

        Args:
            url: URL to crawl
            request: Crawling request configuration
            depth: Current crawl depth (0 for seed URLs)

        Returns:
            CrawlResult for the URL
        """
        start_time = time.time()

        try:
            # Apply rate limiting
            await self.rate_limiter.acquire()

            # Prepare crawl payload
            crawl_payload = self._build_crawl_payload(url, request)

            # Make crawl request (async API)
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Submit crawl task
                response = await client.post(
                    f"{self.base_url}/crawl",
                    json=crawl_payload,
                    headers=self._build_headers("application/json"),
                )
                response.raise_for_status()

                task_data = response.json()
                task_id = task_data["task_id"]

                # Poll for task completion
                crawl_data = await self._wait_for_task_completion(client, task_id)

                # Parse crawl response (screenshots are now included in main response)
                result = await self._parse_crawl_response(
                    url, crawl_data, request, start_time, depth
                )

                return result

        except Exception as e:
            crawl_time = time.time() - start_time
            # Normalize URL to remove trailing slash for consistency
            normalized_url = (
                url.rstrip("/") if url.endswith("/") and url.count("/") == 3 else url
            )

            return CrawlResult(
                url=normalized_url,
                success=False,
                error_message=str(e),
                crawl_time_seconds=crawl_time,
                depth=depth,
            )

    def _build_crawl_payload(self, url: str, request: CrawlRequest) -> dict[str, Any]:
        """
        Build payload for Crawl4AI API request.

        Args:
            url: URL to crawl
            request: Crawling configuration

        Returns:
            Payload dictionary for API request
        """
        # Use minimal payload that works with the API
        payload = {
            "urls": [url],
        }

        # Add screenshot options if requested
        if request.capture_screenshots:
            payload["screenshot"] = True
            payload["screenshot_options"] = {
                "width": request.screenshot_width,
                "height": request.screenshot_height,
                "wait_for": request.screenshot_wait_for,
                "format": "png",
                "full_page": False,
            }

        # Add link extraction options
        if request.scrape_internal_links or request.scrape_external_links:
            payload["extract_links"] = True
            payload["link_types"] = []
            if request.scrape_internal_links:
                payload["link_types"].append("internal")
            if request.scrape_external_links:
                payload["link_types"].append("external")

        return payload

    async def _parse_crawl_response(
        self,
        url: str,
        crawl_data: dict[str, Any],
        request: CrawlRequest,
        start_time: float,
        depth: int = 0,
    ) -> CrawlResult:
        """
        Parse response from Crawl4AI into CrawlResult.

        Args:
            url: Original URL
            crawl_data: Response data from Crawl4AI
            request: Original request
            start_time: Start time for duration calculation
            depth: Current crawl depth

        Returns:
            Parsed CrawlResult
        """
        crawl_time = time.time() - start_time

        try:
            # Extract result from task response
            results = crawl_data.get("results", [])
            if not results:
                return CrawlResult(
                    url=url,
                    success=False,
                    error_message="No results in task response",
                    crawl_time_seconds=crawl_time,
                    depth=depth,
                )

            result_data = results[0]  # Get first result
            status_code = result_data.get("status_code")

            if status_code != 200:
                return CrawlResult(
                    url=url,
                    success=False,
                    error_message=f"HTTP {status_code}",
                    status_code=status_code,
                    crawl_time_seconds=crawl_time,
                    depth=depth,
                )

            # Extract content based on mode
            markdown_content = None
            cleaned_html = None
            metadata = None
            internal_links = None
            external_links = None

            # Always extract markdown
            markdown_data = result_data.get("markdown", {})
            if isinstance(markdown_data, dict):
                markdown_content = markdown_data.get("raw_markdown", "")
            else:
                markdown_content = str(markdown_data) if markdown_data else ""

            # Extract additional content if not markdown-only
            if not request.markdown_only:
                cleaned_html = result_data.get("cleaned_html", "")
                metadata = result_data.get("metadata", {})

            # Extract links if requested
            if request.scrape_internal_links or request.scrape_external_links:
                links_data = result_data.get("links", {})
                if request.scrape_internal_links:
                    internal_links = [
                        link.get("href", "")
                        for link in links_data.get("internal", [])
                        if link.get("href")
                    ]
                if request.scrape_external_links:
                    external_links = [
                        link.get("href", "")
                        for link in links_data.get("external", [])
                        if link.get("href")
                    ]

            # Extract screenshot if present and requested
            screenshot_base64 = None
            screenshot_size = None
            if request.capture_screenshots:
                screenshot_data = result_data.get("screenshot")
                if screenshot_data:
                    # Screenshot is already base64 encoded
                    screenshot_base64 = screenshot_data
                    # Try to extract dimensions from the screenshot
                    try:
                        png_data = base64.b64decode(screenshot_data)
                        screenshot_size = self._get_png_dimensions(png_data)
                    except Exception:
                        # If dimension extraction fails, use requested dimensions
                        screenshot_size = {
                            "width": request.screenshot_width,
                            "height": request.screenshot_height,
                        }

            # Normalize URL to remove trailing slash for consistency
            normalized_url = (
                url.rstrip("/") if url.endswith("/") and url.count("/") == 3 else url
            )

            return CrawlResult(
                url=normalized_url,
                success=True,
                markdown=markdown_content,
                cleaned_html=cleaned_html,
                metadata=metadata,
                internal_links=internal_links,
                external_links=external_links,
                screenshot_base64=screenshot_base64,
                screenshot_size=screenshot_size,
                status_code=status_code,
                crawl_time_seconds=crawl_time,
                depth=depth,
            )

        except Exception as e:
            # Normalize URL to remove trailing slash for consistency
            normalized_url = (
                url.rstrip("/") if url.endswith("/") and url.count("/") == 3 else url
            )

            return CrawlResult(
                url=normalized_url,
                success=False,
                error_message=f"Failed to parse response: {e!s}",
                crawl_time_seconds=crawl_time,
                depth=depth,
            )

    def _get_png_dimensions(self, png_data: bytes) -> dict[str, int] | None:
        """
        Extract dimensions from PNG file headers without using Pillow.

        Args:
            png_data: Binary PNG image data

        Returns:
            Dictionary with width and height, or None if invalid
        """
        try:
            # PNG files start with an 8-byte signature
            if len(png_data) < 24:
                return None

            # Check PNG signature
            if png_data[:8] != b"\x89PNG\r\n\x1a\n":
                return None

            # The IHDR chunk starts at byte 8 and contains width/height
            # IHDR chunk: [length:4][type:4][width:4][height:4][bit_depth:1][color_type:1][compression:1][filter:1][interlace:1][crc:4]
            ihdr_start = 8

            # Check if we have enough data for IHDR
            if len(png_data) < ihdr_start + 8:
                return None

            # Skip chunk length (4 bytes) and chunk type (4 bytes)
            width_start = ihdr_start + 8
            height_start = width_start + 4

            if len(png_data) < height_start + 4:
                return None

            # Extract width and height (big-endian 32-bit integers)
            width = struct.unpack(">I", png_data[width_start : width_start + 4])[0]
            height = struct.unpack(">I", png_data[height_start : height_start + 4])[0]

            return {"width": width, "height": height}

        except Exception:
            return None

    def _request_to_options(self, request: CrawlRequest) -> dict[str, Any]:
        """
        Convert CrawlRequest to options dictionary for caching.

        Args:
            request: CrawlRequest instance

        Returns:
            Options dictionary
        """
        options = {
            "markdown_only": request.markdown_only,
            "scrape_internal_links": request.scrape_internal_links,
            "scrape_external_links": request.scrape_external_links,
            "capture_screenshots": request.capture_screenshots,
            "follow_internal_links": request.follow_internal_links,
            "follow_external_links": request.follow_external_links,
            "max_depth": request.max_depth,
            "max_pages": request.max_pages,
        }

        if request.capture_screenshots:
            options.update(
                {
                    "screenshot_width": request.screenshot_width,
                    "screenshot_height": request.screenshot_height,
                    "screenshot_wait_for": request.screenshot_wait_for,
                }
            )

        return options

    def get_cache_stats(self) -> dict[str, Any]:
        """
        Get cache and service statistics.

        Returns:
            Statistics dictionary
        """
        cache_stats = self.cache.get_stats()

        return {
            "service": "crawling",
            "cache_size": cache_stats["cache_size"],
            "cache_ttl_hours": cache_stats["cache_ttl_hours"],
            "rate_limiter_active": True,
            "crawl4ai_instance": self.base_url,
            "oldest_entry_age_minutes": cache_stats.get("oldest_entry_age_minutes"),
            "expired_entries": cache_stats.get("expired_entries", 0),
        }

    def clear_cache(self) -> int:
        """
        Clear all cached crawling results.

        Returns:
            Number of entries cleared
        """
        return self.cache.clear()

    async def get_health_response(self) -> CrawlingHealthResponse:
        """
        Get comprehensive health check response.

        Returns:
            CrawlingHealthResponse with service status
        """
        # Get basic service stats
        stats = self.get_cache_stats()

        # Check Crawl4AI health
        health_check = await self.health_check()

        return CrawlingHealthResponse(
            service="crawling",
            status="healthy" if health_check["crawl4ai_healthy"] else "degraded",
            cache_size=stats["cache_size"],
            cache_ttl_hours=stats["cache_ttl_hours"],
            rate_limiter_active=stats["rate_limiter_active"],
            crawl4ai_instance=stats["crawl4ai_instance"],
            crawl4ai_healthy=health_check["crawl4ai_healthy"],
            crawl4ai_response=health_check.get("crawl4ai_response"),
        )

    def clear_cache_response(self) -> CacheClearResponse:
        """
        Clear cache and return formatted response.

        Returns:
            CacheClearResponse with operation details
        """
        cleared_count = self.clear_cache()
        return CacheClearResponse.create_success(cleared_count)

    async def invalidate_url_cache(self, url: str) -> int:
        """
        Invalidate all cached results for a specific URL.

        Args:
            url: URL to invalidate

        Returns:
            Number of cache entries invalidated
        """
        return self.cache.invalidate_url(url)

    def cleanup_expired_cache(self) -> int:
        """
        Clean up expired cache entries.

        Returns:
            Number of expired entries removed
        """
        return self.cache.cleanup_expired()


# Global service instance
_crawling_service: CrawlingService | None = None


def get_crawling_service() -> CrawlingService:
    """
    Get the global crawling service instance.

    Returns:
        CrawlingService instance
    """
    global _crawling_service
    if _crawling_service is None:
        _crawling_service = CrawlingService()
    return _crawling_service

"""
Pydantic models for crawling functionality.

This module defines the data models used for crawling requests and responses,
including support for screenshot capture with custom dimensions.
"""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, HttpUrl, field_validator, model_validator


class CrawlRequest(BaseModel):
    """
    Request model for crawling URLs.

    Supports multi-URL crawling, link extraction, screenshots with custom dimensions,
    and various caching options.
    """

    urls: list[HttpUrl] = Field(
        ...,
        min_length=1,
        max_length=10,
        description="List of URLs to crawl (1-10 URLs maximum)",
    )

    # Content extraction options
    markdown_only: bool = Field(
        default=False,
        description="Return only markdown content (excludes HTML, metadata, links)",
    )

    scrape_internal_links: bool = Field(
        default=False, description="Extract internal links from crawled pages"
    )

    scrape_external_links: bool = Field(
        default=False, description="Extract external links from crawled pages"
    )

    # Recursive crawling options
    follow_internal_links: bool = Field(
        default=False,
        description="Follow and crawl discovered internal links recursively",
    )

    follow_external_links: bool = Field(
        default=False,
        description="Follow and crawl discovered external links recursively",
    )

    max_depth: int = Field(
        default=1,
        ge=1,
        le=5,
        description="Maximum crawl depth when following links (1-5, max 3 for external links)",
    )

    max_pages: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum total pages to crawl when following links (1-50, max 20 for external links)",
    )

    # Screenshot options
    capture_screenshots: bool = Field(
        default=False, description="Capture screenshots of the pages"
    )

    screenshot_width: int | None = Field(
        default=1920,
        ge=320,
        le=3840,
        description="Screenshot viewport width in pixels (320-3840)",
    )

    screenshot_height: int | None = Field(
        default=1080,
        ge=240,
        le=2160,
        description="Screenshot viewport height in pixels (240-2160)",
    )

    screenshot_wait_for: int | None = Field(
        default=2,
        ge=0,
        le=30,
        description="Seconds to wait before taking screenshot (0-30)",
    )

    # Caching options
    cache_mode: Literal["enabled", "disabled", "bypass"] = Field(
        default="enabled",
        description="Cache behavior: enabled (use cache), disabled (no cache), bypass (ignore cache)",
    )

    @field_validator("urls")
    @classmethod
    def validate_urls(cls, v: list[HttpUrl]) -> list[HttpUrl]:
        """
        Validate URL list constraints.

        Args:
            v: List of URLs to validate

        Returns:
            Validated list of URLs

        Raises:
            ValueError: If validation fails
        """
        if not v:
            raise ValueError("At least one URL is required")

        if len(v) > 10:
            raise ValueError("Maximum 10 URLs allowed per request")

        # Ensure URLs use HTTP/HTTPS schemes
        for url in v:
            if url.scheme not in ("http", "https"):
                raise ValueError(f"URL {url} must use http or https scheme")

        return v

    @model_validator(mode="after")
    def validate_screenshot_options(self) -> "CrawlRequest":
        """
        Validate screenshot-related options.

        Returns:
            Validated model instance

        Raises:
            ValueError: If screenshot options are invalid
        """
        if self.capture_screenshots:
            if self.screenshot_width is None or self.screenshot_height is None:
                raise ValueError(
                    "Screenshot dimensions are required when capture_screenshots=True"
                )

            # Validate aspect ratio isn't too extreme
            aspect_ratio = self.screenshot_width / self.screenshot_height
            if aspect_ratio < 0.5 or aspect_ratio > 4.0:
                raise ValueError(
                    "Screenshot aspect ratio must be between 0.5:1 and 4:1"
                )

            # Validate pixel count to prevent excessive memory usage
            pixel_count = self.screenshot_width * self.screenshot_height
            if pixel_count > 8_294_400:  # 4K limit (3840 x 2160)
                raise ValueError(
                    "Screenshot dimensions exceed maximum pixel count (4K resolution limit)"
                )

        # Validate recursive crawling options
        if self.follow_internal_links and not self.scrape_internal_links:
            raise ValueError(
                "follow_internal_links requires scrape_internal_links to be enabled"
            )

        if self.follow_external_links and not self.scrape_external_links:
            raise ValueError(
                "follow_external_links requires scrape_external_links to be enabled"
            )

        # When following links, ensure URLs list isn't too large
        if (self.follow_internal_links or self.follow_external_links) and len(
            self.urls
        ) > 3:
            raise ValueError(
                "When following links is enabled, maximum 3 seed URLs allowed"
            )

        # Additional safety: When following external links, reduce max limits
        if self.follow_external_links:
            if self.max_depth > 3:
                raise ValueError(
                    "When following external links, maximum depth is 3 for security"
                )
            if self.max_pages > 20:
                raise ValueError(
                    "When following external links, maximum pages is 20 for security"
                )

        return self


class CrawlResult(BaseModel):
    """
    Result model for individual URL crawling.

    Contains the extracted content, metadata, and any errors encountered.
    """

    url: str = Field(..., description="The crawled URL")

    success: bool = Field(..., description="Whether the crawl was successful")

    depth: int = Field(default=0, description="Crawl depth (0 for seed URLs)")

    # Content fields (optional based on success and options)
    markdown: str | None = Field(default=None, description="Extracted markdown content")

    cleaned_html: str | None = Field(
        default=None,
        description="Cleaned HTML content (excluded in markdown_only mode)",
    )

    metadata: dict[str, Any] | None = Field(
        default=None,
        description="Page metadata (title, description, etc.) - excluded in markdown_only mode",
    )

    # Link extraction results
    internal_links: list[str] | None = Field(
        default=None, description="Internal links found on the page"
    )

    external_links: list[str] | None = Field(
        default=None, description="External links found on the page"
    )

    # Screenshot results
    screenshot_base64: str | None = Field(
        default=None, description="Base64-encoded screenshot image data"
    )

    screenshot_size: dict[str, int] | None = Field(
        default=None, description="Screenshot dimensions {width: int, height: int}"
    )

    # Error information
    error_message: str | None = Field(
        default=None, description="Error message if crawl failed"
    )

    status_code: int | None = Field(
        default=None, description="HTTP status code from the crawl"
    )

    # Performance metrics
    crawl_time_seconds: float | None = Field(
        default=None, description="Time taken to crawl this URL in seconds"
    )

    @model_validator(mode="after")
    def validate_success_consistency(self) -> "CrawlResult":
        """
        Validate that success flag is consistent with other fields.

        Returns:
            Validated model instance

        Raises:
            ValueError: If success flag is inconsistent
        """
        if self.success:
            # Successful crawls should have at least markdown content
            if not self.markdown:
                raise ValueError("Successful crawls must have markdown content")
        else:
            # Failed crawls should have an error message
            if not self.error_message:
                raise ValueError("Failed crawls must have an error message")

        # Screenshot consistency
        if self.screenshot_base64 and not self.screenshot_size:
            raise ValueError("Screenshot data must include size information")

        return self


class CrawlingResponse(BaseModel):
    """
    Response model for crawling operations.

    Contains summary statistics and individual results for all crawled URLs.
    """

    total_urls: int = Field(..., description="Total number of URLs requested")

    successful_crawls: int = Field(
        ..., description="Number of successfully crawled URLs"
    )

    failed_crawls: int = Field(..., description="Number of failed crawl attempts")

    cached_results: int = Field(
        default=0, description="Number of results served from cache"
    )

    results: list[CrawlResult] = Field(
        ..., description="Individual crawl results for each URL"
    )

    timestamp: str = Field(..., description="Response timestamp in ISO format")

    total_time_seconds: float | None = Field(
        default=None, description="Total time taken for all crawls in seconds"
    )

    @model_validator(mode="after")
    def validate_response_consistency(self) -> "CrawlingResponse":
        """
        Validate response consistency and statistics.

        Returns:
            Validated model instance

        Raises:
            ValueError: If response data is inconsistent
        """
        # Check URL count consistency
        if len(self.results) != self.total_urls:
            raise ValueError("Number of results must match total_urls")

        # Check success/failure counts
        actual_successful = sum(1 for result in self.results if result.success)
        actual_failed = sum(1 for result in self.results if not result.success)

        if actual_successful != self.successful_crawls:
            raise ValueError(
                f"successful_crawls ({self.successful_crawls}) doesn't match actual successful results ({actual_successful})"
            )

        if actual_failed != self.failed_crawls:
            raise ValueError(
                f"failed_crawls ({self.failed_crawls}) doesn't match actual failed results ({actual_failed})"
            )

        # Check total consistency
        if self.successful_crawls + self.failed_crawls != self.total_urls:
            raise ValueError("successful_crawls + failed_crawls must equal total_urls")

        # Cached results can't exceed total URLs
        if self.cached_results > self.total_urls:
            raise ValueError("cached_results cannot exceed total_urls")

        return self

    @classmethod
    def create_from_results(
        cls,
        results: list[CrawlResult],
        cached_count: int = 0,
        total_time: float | None = None,
    ) -> "CrawlingResponse":
        """
        Create a CrawlingResponse from a list of CrawlResult objects.

        Args:
            results: List of crawl results
            cached_count: Number of cached results
            total_time: Total processing time in seconds

        Returns:
            CrawlingResponse instance
        """
        successful = sum(1 for result in results if result.success)
        failed = len(results) - successful

        return cls(
            total_urls=len(results),
            successful_crawls=successful,
            failed_crawls=failed,
            cached_results=cached_count,
            results=results,
            timestamp=datetime.now().isoformat(),
            total_time_seconds=total_time,
        )


# Health check response model
class CrawlingHealthResponse(BaseModel):
    """
    Health check response for crawling service.
    """

    service: str = Field(default="crawling", description="Service name")

    status: str = Field(..., description="Service status (healthy/unhealthy)")

    cache_size: int = Field(..., description="Number of items in cache")

    cache_ttl_hours: int = Field(..., description="Cache TTL in hours")

    rate_limiter_active: bool = Field(
        ..., description="Whether rate limiting is active"
    )

    crawl4ai_instance: str = Field(..., description="Crawl4AI instance URL")

    crawl4ai_healthy: bool | None = Field(
        default=None, description="Whether Crawl4AI service is responding"
    )

    crawl4ai_response: dict[str, Any] | None = Field(
        default=None, description="Response from Crawl4AI health check"
    )


# Cache clear response model
class CacheClearResponse(BaseModel):
    """
    Response model for cache clearing operations.
    """

    message: str = Field(..., description="Success message")

    cleared_entries: int = Field(..., description="Number of cache entries cleared")

    timestamp: str = Field(..., description="Operation timestamp in ISO format")

    @classmethod
    def create_success(cls, cleared_count: int) -> "CacheClearResponse":
        """
        Create a successful cache clear response.

        Args:
            cleared_count: Number of entries cleared

        Returns:
            CacheClearResponse instance
        """
        return cls(
            message=f"Cache cleared successfully. {cleared_count} entries removed.",
            cleared_entries=cleared_count,
            timestamp=datetime.now().isoformat(),
        )

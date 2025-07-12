import time
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from models.crawling import CrawlRequest
from services.crawling import CrawlingService


def create_async_api_mocks(
    task_completion_response, screenshot_response=None, fail_screenshot=False
):
    """Helper to create mocks for the async Crawl4AI API pattern."""
    task_submission = {"task_id": f"test-task-{int(time.time())}"}

    mock_post_response = MagicMock()
    mock_post_response.json.return_value = task_submission
    mock_post_response.raise_for_status.return_value = None

    mock_get_response = MagicMock()
    mock_get_response.json.return_value = task_completion_response
    mock_get_response.raise_for_status.return_value = None

    mock_client_instance = AsyncMock()
    mock_client_instance.post.return_value = mock_post_response
    mock_client_instance.get.return_value = mock_get_response

    if screenshot_response:
        mock_screenshot_response = MagicMock()
        mock_screenshot_response.content = screenshot_response
        if fail_screenshot:
            mock_screenshot_response.raise_for_status.side_effect = (
                httpx.HTTPStatusError(
                    "404 Not Found", request=MagicMock(), response=MagicMock()
                )
            )
        else:
            mock_screenshot_response.raise_for_status.return_value = None
        # Mock multiple post calls (crawl + screenshot)
        mock_client_instance.post.side_effect = [
            mock_post_response,
            mock_screenshot_response,
        ]

    return mock_client_instance


def create_failed_task_response():
    """Helper to create a failed task response."""
    return {
        "status": "completed",
        "results": [{"status_code": 404, "error": "Not found"}],
    }


def create_success_task_response(url="https://example.com", include_links=False):
    """Helper to create a successful task response."""
    result = {
        "status_code": 200,
        "markdown": {"raw_markdown": "# Test Page"},
        "cleaned_html": "<h1>Test Page</h1>",
        "metadata": {"title": "Test"},
    }

    if include_links:
        result["links"] = {
            "internal": [{"href": f"{url}/about"}],
            "external": [{"href": "https://google.com"}],
        }

    return {"status": "completed", "results": [result]}


@pytest.mark.asyncio
async def test_crawling_service_health_check_success():
    """Test successful Crawl4AI health check."""
    service = CrawlingService()

    mock_health_response = {"status": "healthy", "version": "0.6.0"}

    with patch("httpx.AsyncClient") as mock_client:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_health_response
        mock_response.raise_for_status.return_value = None

        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        result = await service.health_check()

        assert result["crawl4ai_healthy"] is True
        assert "crawl4ai_response" in result
        assert result["crawl4ai_response"] == mock_health_response


@pytest.mark.asyncio
async def test_crawling_service_health_check_failure():
    """Test Crawl4AI health check failure."""
    service = CrawlingService()

    with patch("httpx.AsyncClient") as mock_client:
        mock_client_instance = AsyncMock()
        mock_client_instance.get.side_effect = httpx.TimeoutException("Timeout")
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        result = await service.health_check()

        assert result["crawl4ai_healthy"] is False
        assert "error" in result


@pytest.mark.asyncio
async def test_crawl_single_url_success():
    """Test successful single URL crawling with async API."""
    service = CrawlingService()

    # Mock task submission response
    _mock_task_submission = {"task_id": "test-task-123"}

    # Mock task completion response (new async format)
    mock_task_completion = {
        "status": "completed",
        "results": [
            {
                "status_code": 200,
                "markdown": {"raw_markdown": "# Test Page"},
                "cleaned_html": "<h1>Test Page</h1>",
                "metadata": {"title": "Test"},
                "links": {
                    "internal": [{"href": "https://example.com/about"}],
                    "external": [{"href": "https://google.com"}],
                },
            }
        ],
    }

    with patch("httpx.AsyncClient") as mock_client:
        mock_client_instance = create_async_api_mocks(mock_task_completion)
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        crawl_request = CrawlRequest(
            urls=["https://example.com"],
            scrape_internal_links=True,
            scrape_external_links=True,
            markdown_only=False,
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
    """Test markdown-only crawling with async API."""
    service = CrawlingService()

    # Mock task submission response
    _mock_task_submission = {"task_id": "test-task-456"}

    # Mock task completion response for markdown-only
    mock_task_completion = {
        "status": "completed",
        "results": [
            {
                "status_code": 200,
                "markdown": {"raw_markdown": "# Test Page"},
                "cleaned_html": "<h1>Test Page</h1>",
                "metadata": {"title": "Test"},
            }
        ],
    }

    with patch("httpx.AsyncClient") as mock_client:
        mock_client_instance = create_async_api_mocks(mock_task_completion)
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        crawl_request = CrawlRequest(urls=["https://example.com"], markdown_only=True)

        result = await service.crawl_urls(crawl_request)

        crawl_result = result.results[0]
        assert crawl_result.markdown == "# Test Page"
        assert crawl_result.cleaned_html is None
        assert crawl_result.metadata is None


@pytest.mark.asyncio
async def test_crawl_with_screenshots():
    """Test crawling with screenshot capture using async API."""
    service = CrawlingService()

    # Mock screenshot binary data (16x16 PNG)
    mock_image_data = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x19tEXtSoftware\x00Adobe ImageReadyq\xc9e<\x00\x00\x00\x0eIDATx\xdab\xf8\x00\x00\x00\x01\x00\x01\x03\x02\xfe\x1f\x00\x00\x00\x00IEND\xaeB`\x82"

    # Convert to base64 for the mock response
    import base64

    screenshot_base64 = base64.b64encode(mock_image_data).decode("utf-8")

    # Mock task completion response with screenshot included
    mock_task_completion = {
        "status": "completed",
        "results": [
            {
                "status_code": 200,
                "markdown": {"raw_markdown": "# Test Page"},
                "cleaned_html": "<h1>Test Page</h1>",
                "screenshot": screenshot_base64,  # Screenshot now included in main response
            }
        ],
    }

    with patch("httpx.AsyncClient") as mock_client:
        mock_client_instance = create_async_api_mocks(mock_task_completion)
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        crawl_request = CrawlRequest(
            urls=["https://example.com"],
            capture_screenshots=True,
            screenshot_wait_for=3,
            screenshot_width=1280,
            screenshot_height=720,
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
    """Test graceful handling of screenshot failures with async API."""
    service = CrawlingService()

    # Mock successful crawl task completion
    mock_task_completion = {
        "status": "completed",
        "results": [{"status_code": 200, "markdown": {"raw_markdown": "# Test Page"}}],
    }

    with patch("httpx.AsyncClient") as mock_client:
        # Use helper to create mocks with failed screenshot
        mock_client_instance = create_async_api_mocks(
            mock_task_completion,
            screenshot_response=b"fake-image-data",
            fail_screenshot=True,
        )
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        crawl_request = CrawlRequest(
            urls=["https://example.com"], capture_screenshots=True
        )

        result = await service.crawl_urls(crawl_request)

        # Crawl should still succeed even if screenshot fails
        assert result.successful_crawls == 1
        crawl_result = result.results[0]
        assert crawl_result.success is True
        assert crawl_result.markdown == "# Test Page"
        assert crawl_result.screenshot_base64 is None  # Screenshot failed gracefully


@pytest.mark.asyncio
async def test_crawl_multiple_urls():
    """Test crawling multiple URLs with async API."""
    service = CrawlingService()

    # Use helper to create success response
    mock_task_completion = create_success_task_response()

    with patch("httpx.AsyncClient") as mock_client:
        mock_client_instance = create_async_api_mocks(mock_task_completion)
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        crawl_request = CrawlRequest(
            urls=["https://example.com", "https://test.com", "https://demo.com"],
            markdown_only=True,
        )

        result = await service.crawl_urls(crawl_request)

        assert result.total_urls == 3
        assert result.successful_crawls == 3
        assert result.failed_crawls == 0
        assert len(result.results) == 3

        # All URLs should be represented (normalized without trailing slash)
        urls = {result.url for result in result.results}
        assert urls == {"https://example.com", "https://test.com", "https://demo.com"}


@pytest.mark.asyncio
async def test_crawl_mixed_success_failure():
    """Test crawling with mixed success and failure results using async API."""
    service = CrawlingService()

    # Mock different responses for success.com and failure.com
    def mock_post_side_effect(_url, **kwargs):
        """Mock task submission for each URL."""
        payload = kwargs.get("json", {})
        crawl_urls = payload.get("urls", [])

        if crawl_urls and "success.com" in crawl_urls[0]:
            # Success task submission
            response = MagicMock()
            response.json.return_value = {"task_id": "success-task-123"}
            response.raise_for_status.return_value = None
            return response
        else:
            # Failure task submission (HTTP error)
            response = MagicMock()
            response.raise_for_status.side_effect = httpx.HTTPStatusError(
                "Not found", request=None, response=MagicMock(status_code=404)
            )
            return response

    def mock_get_side_effect(url, **_kwargs):
        """Mock task polling responses."""
        if "success-task-123" in url:
            # Success task completion
            response = MagicMock()
            response.json.return_value = {
                "status": "completed",
                "results": [
                    {
                        "status_code": 200,
                        "markdown": {"raw_markdown": "# Success"},
                    }
                ],
            }
            response.raise_for_status.return_value = None
            return response
        else:
            # This shouldn't be called for failed submissions
            response = MagicMock()
            response.raise_for_status.side_effect = Exception("Unexpected call")
            return response

    with patch("httpx.AsyncClient") as mock_client:
        mock_client_instance = AsyncMock()
        mock_client_instance.post.side_effect = mock_post_side_effect
        mock_client_instance.get.side_effect = mock_get_side_effect
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        crawl_request = CrawlRequest(
            urls=["https://success.com", "https://failure.com"]
        )

        result = await service.crawl_urls(crawl_request)

        assert result.total_urls == 2
        assert result.successful_crawls == 1
        assert result.failed_crawls == 1

        # Find success and failure results
        success_result = next(r for r in result.results if "success.com" in r.url)
        failure_result = next(r for r in result.results if "failure.com" in r.url)

        assert success_result.success is True
        assert failure_result.success is False
        assert failure_result.error_message is not None


@pytest.mark.asyncio
async def test_crawl_caching_behavior():
    """Test that caching works correctly with async API."""
    service = CrawlingService()

    # Mock successful task completion
    mock_task_completion = {
        "status": "completed",
        "results": [
            {"status_code": 200, "markdown": {"raw_markdown": "# Cached Page"}}
        ],
    }

    with patch("httpx.AsyncClient") as mock_client:
        mock_client_instance = create_async_api_mocks(mock_task_completion)
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        crawl_request = CrawlRequest(urls=["https://example.com"], cache_mode="enabled")

        # First call
        result1 = await service.crawl_urls(crawl_request)
        assert result1.cached_results == 0  # No cache hits on first call

        # Second call should hit cache
        result2 = await service.crawl_urls(crawl_request)
        assert result2.cached_results == 1  # Cache hit

        # API should only be called once (POST + GET for first call only)
        assert mock_client_instance.post.call_count == 1
        assert mock_client_instance.get.call_count == 1


@pytest.mark.asyncio
async def test_crawl_cache_bypass():
    """Test cache bypass functionality."""
    service = CrawlingService()

    mock_crawl4ai_response = {
        "result": {"status_code": 200, "markdown": {"raw_markdown": "# No Cache Page"}}
    }

    with patch("httpx.AsyncClient") as mock_client:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_crawl4ai_response
        mock_response.raise_for_status.return_value = None

        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        crawl_request = CrawlRequest(urls=["https://example.com"], cache_mode="bypass")

        # First call
        await service.crawl_urls(crawl_request)

        # Second call with bypass should not use cache
        result2 = await service.crawl_urls(crawl_request)
        assert result2.cached_results == 0  # No cache hits

        # API should be called twice
        assert mock_client_instance.post.call_count == 2


@pytest.mark.asyncio
async def test_rate_limiting_enforced():
    """Test that rate limiting is enforced."""
    service = CrawlingService()

    mock_crawl4ai_response = {
        "result": {"status_code": 200, "markdown": {"raw_markdown": "# Rate Limited"}}
    }

    with patch("httpx.AsyncClient") as mock_client:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_crawl4ai_response
        mock_response.raise_for_status.return_value = None

        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        # Clear cache to ensure API calls
        service.cache.clear()

        start_time = time.time()

        # Two different URLs to avoid cache
        crawl_request = CrawlRequest(
            urls=["https://test1.com", "https://test2.com"], cache_mode="disabled"
        )

        await service.crawl_urls(crawl_request)

        elapsed = time.time() - start_time

        # Should take at least 1 second due to rate limiting (5 req/sec = 0.2s interval)
        # But with 2 URLs, we should see some delay
        assert elapsed >= 0.1  # Allow some tolerance for test execution


@pytest.mark.asyncio
async def test_png_dimensions_parsing():
    """Test PNG dimensions extraction without Pillow."""
    service = CrawlingService()

    # Valid PNG header with 16x16 dimensions
    png_data = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa"

    dimensions = service._get_png_dimensions(png_data)
    assert dimensions is not None
    assert dimensions["width"] == 16
    assert dimensions["height"] == 16


@pytest.mark.asyncio
async def test_png_dimensions_invalid_data():
    """Test PNG dimensions parsing with invalid data."""
    service = CrawlingService()

    # Invalid PNG data
    invalid_data = b"not a png file"

    dimensions = service._get_png_dimensions(invalid_data)
    assert dimensions is None

    # Too short data
    short_data = b"\x89PNG"
    dimensions = service._get_png_dimensions(short_data)
    assert dimensions is None


def test_cache_stats():
    """Test cache statistics."""
    service = CrawlingService()

    stats = service.get_cache_stats()

    assert "cache_size" in stats
    assert "cache_ttl_hours" in stats
    assert "rate_limiter_active" in stats
    assert "crawl4ai_instance" in stats
    assert stats["rate_limiter_active"] is True


def test_clear_cache():
    """Test cache clearing."""
    service = CrawlingService()

    # Add something to cache
    service.cache.set("https://test.com", {"markdown_only": True}, {"success": True})
    assert service.cache.size() > 0

    # Clear cache
    service.clear_cache()
    assert service.cache.size() == 0


@pytest.mark.asyncio
async def test_crawl_url_validation():
    """Test URL validation in crawl requests."""
    CrawlingService()

    # Test with valid URLs - this should work fine
    crawl_request = CrawlRequest(urls=["https://example.com", "http://test.com"])

    # The request should be valid (no exception raised)
    assert len(crawl_request.urls) == 2


@pytest.mark.asyncio
async def test_screenshot_custom_dimensions():
    """Test screenshot capture with custom dimensions using async API."""
    service = CrawlingService()

    # Mock screenshot with custom dimensions (1280x720 PNG)
    custom_png_data = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x05\x00\x00\x00\x02\xd0\x08\x06\x00\x00\x00\x1f\xf3\xffa"

    # Convert to base64 for the mock response
    import base64

    screenshot_base64 = base64.b64encode(custom_png_data).decode("utf-8")

    # Mock successful task completion with screenshot included
    mock_task_completion = {
        "status": "completed",
        "results": [
            {
                "status_code": 200,
                "markdown": {"raw_markdown": "# Test"},
                "screenshot": screenshot_base64,  # Screenshot now included in main response
            }
        ],
    }

    with patch("httpx.AsyncClient") as mock_client:
        mock_client_instance = create_async_api_mocks(mock_task_completion)
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        crawl_request = CrawlRequest(
            urls=["https://example.com"],
            capture_screenshots=True,
            screenshot_width=1280,
            screenshot_height=720,
        )

        result = await service.crawl_urls(crawl_request)

        crawl_result = result.results[0]
        assert crawl_result.success is True
        assert crawl_result.screenshot_base64 is not None
        # Dimensions should be extracted from PNG
        assert crawl_result.screenshot_size["width"] == 1280
        assert crawl_result.screenshot_size["height"] == 720


@pytest.mark.asyncio
async def test_recursive_crawling_simple():
    """Test recursive crawling with simple internal links."""
    service = CrawlingService()

    # Create a mock that returns different responses for different URLs
    call_count = 0

    def create_response_for_url(url):
        """Create appropriate response based on URL."""
        if "example.com" in url and "about" not in url:
            # Root page with internal links
            return {
                "status": "completed",
                "results": [
                    {
                        "status_code": 200,
                        "markdown": {"raw_markdown": "# Home Page"},
                        "links": {
                            "internal": [
                                {"href": "/about"},
                                {"href": "https://example.com/contact"},
                            ],
                            "external": [{"href": "https://google.com"}],
                        },
                    }
                ],
            }
        elif "about" in url:
            # About page with no more links
            return {
                "status": "completed",
                "results": [
                    {
                        "status_code": 200,
                        "markdown": {"raw_markdown": "# About Page"},
                        "links": {"internal": [], "external": []},
                    }
                ],
            }
        elif "contact" in url:
            # Contact page with no more links
            return {
                "status": "completed",
                "results": [
                    {
                        "status_code": 200,
                        "markdown": {"raw_markdown": "# Contact Page"},
                        "links": {"internal": [], "external": []},
                    }
                ],
            }
        else:
            return create_failed_task_response()

    with patch("httpx.AsyncClient") as mock_client:
        # Mock the post and get methods to handle multiple calls
        post_responses = []
        get_responses = []

        def mock_post(*_args, **_kwargs):
            nonlocal call_count
            call_count += 1
            response = MagicMock()
            response.json.return_value = {"task_id": f"task-{call_count}"}
            response.raise_for_status.return_value = None
            post_responses.append(response)
            return response

        def mock_get(*_args, **_kwargs):
            # Extract URL from the call to determine which response to return
            url = _args[0] if _args else _kwargs.get("url", "")

            # Figure out which URL was crawled based on call order
            if "task-1" in url:
                response_data = create_response_for_url("https://example.com")
            elif "task-2" in url:
                response_data = create_response_for_url("https://example.com/about")
            elif "task-3" in url:
                response_data = create_response_for_url("https://example.com/contact")
            else:
                response_data = create_failed_task_response()

            response = MagicMock()
            response.json.return_value = response_data
            response.raise_for_status.return_value = None
            get_responses.append(response)
            return response

        mock_client_instance = AsyncMock()
        mock_client_instance.post.side_effect = mock_post
        mock_client_instance.get.side_effect = mock_get
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        # Clear cache to ensure all URLs are crawled
        service.cache.clear()

        crawl_request = CrawlRequest(
            urls=["https://example.com"],
            scrape_internal_links=True,
            follow_internal_links=True,
            max_depth=2,
            max_pages=10,
            cache_mode="disabled",  # Disable cache for predictable testing
        )

        result = await service.crawl_urls(crawl_request)

        # Should have crawled the root page and discovered links
        assert result.total_urls == 3  # Root + about + contact
        assert result.successful_crawls == 3
        assert result.failed_crawls == 0

        # Check depth levels
        depths = {r.url: r.depth for r in result.results}
        assert depths["https://example.com"] == 0  # Seed URL (normalized)
        assert depths["https://example.com/about"] == 1  # Discovered from root
        assert depths["https://example.com/contact"] == 1  # Discovered from root


@pytest.mark.asyncio
async def test_recursive_crawling_max_depth():
    """Test that recursive crawling respects max_depth limit."""
    service = CrawlingService()

    # Create a chain of pages that link to each other
    def create_response_for_depth(depth):
        if depth < 5:  # Create links up to depth 5
            return {
                "status": "completed",
                "results": [
                    {
                        "status_code": 200,
                        "markdown": {"raw_markdown": f"# Page at depth {depth}"},
                        "links": {
                            "internal": [{"href": f"/page{depth + 1}"}],
                            "external": [],
                        },
                    }
                ],
            }
        else:
            return {
                "status": "completed",
                "results": [
                    {
                        "status_code": 200,
                        "markdown": {"raw_markdown": f"# Page at depth {depth}"},
                        "links": {"internal": [], "external": []},
                    }
                ],
            }

    call_count = 0

    with patch("httpx.AsyncClient") as mock_client:

        def mock_post(*_args, **_kwargs):
            nonlocal call_count
            call_count += 1
            response = MagicMock()
            response.json.return_value = {"task_id": f"task-{call_count}"}
            response.raise_for_status.return_value = None
            return response

        def mock_get(*_args, **_kwargs):
            url = _args[0] if _args else _kwargs.get("url", "")

            # Map task IDs to depths
            if "task-1" in url:
                response_data = create_response_for_depth(0)
            elif "task-2" in url:
                response_data = create_response_for_depth(1)
            elif "task-3" in url:
                response_data = create_response_for_depth(2)
            else:
                response_data = create_failed_task_response()

            response = MagicMock()
            response.json.return_value = response_data
            response.raise_for_status.return_value = None
            return response

        mock_client_instance = AsyncMock()
        mock_client_instance.post.side_effect = mock_post
        mock_client_instance.get.side_effect = mock_get
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        # Clear cache
        service.cache.clear()

        crawl_request = CrawlRequest(
            urls=["https://example.com"],
            scrape_internal_links=True,
            follow_internal_links=True,
            max_depth=2,  # Limit to depth 2
            max_pages=10,
            cache_mode="disabled",
        )

        result = await service.crawl_urls(crawl_request)

        # Should have crawled only up to depth 1 (seed + 1 level)
        assert result.total_urls == 2  # depth 0 and depth 1 only
        assert all(r.depth <= 1 for r in result.results)


@pytest.mark.asyncio
async def test_recursive_crawling_max_pages():
    """Test that recursive crawling respects max_pages limit."""
    service = CrawlingService()

    # Create a page with many internal links
    def create_response_with_many_links():
        return {
            "status": "completed",
            "results": [
                {
                    "status_code": 200,
                    "markdown": {"raw_markdown": "# Page with many links"},
                    "links": {
                        "internal": [{"href": f"/page{i}"} for i in range(10)],
                        "external": [],
                    },
                }
            ],
        }

    call_count = 0

    with patch("httpx.AsyncClient") as mock_client:

        def mock_post(*_args, **_kwargs):
            nonlocal call_count
            call_count += 1
            response = MagicMock()
            response.json.return_value = {"task_id": f"task-{call_count}"}
            response.raise_for_status.return_value = None
            return response

        def mock_get(*_args, **_kwargs):
            # Always return a page with many links
            response = MagicMock()
            response.json.return_value = create_response_with_many_links()
            response.raise_for_status.return_value = None
            return response

        mock_client_instance = AsyncMock()
        mock_client_instance.post.side_effect = mock_post
        mock_client_instance.get.side_effect = mock_get
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        # Clear cache
        service.cache.clear()

        crawl_request = CrawlRequest(
            urls=["https://example.com"],
            scrape_internal_links=True,
            follow_internal_links=True,
            max_depth=5,
            max_pages=3,  # Limit to 3 pages total
            cache_mode="disabled",
        )

        result = await service.crawl_urls(crawl_request)

        # Should have crawled exactly 3 pages
        assert result.total_urls == 3
        assert len(result.results) == 3


@pytest.mark.asyncio
async def test_recursive_crawling_same_domain_only():
    """Test that recursive crawling only follows same-domain links."""
    service = CrawlingService()

    # Create a page with mixed internal and external links
    mock_response = {
        "status": "completed",
        "results": [
            {
                "status_code": 200,
                "markdown": {"raw_markdown": "# Page with mixed links"},
                "links": {
                    "internal": [
                        {"href": "/internal-page"},
                        {"href": "https://example.com/same-domain"},
                        {"href": "https://different.com/external"},  # Different domain
                    ],
                    "external": [{"href": "https://google.com"}],
                },
            }
        ],
    }

    # Track which URLs are crawled
    crawled_urls = []

    with patch("httpx.AsyncClient") as mock_client:

        def mock_post(*_args, **_kwargs):
            payload = _kwargs.get("json", {})
            urls = payload.get("urls", [])
            if urls:
                crawled_urls.append(urls[0])

            response = MagicMock()
            response.json.return_value = {"task_id": f"task-{len(crawled_urls)}"}
            response.raise_for_status.return_value = None
            return response

        def mock_get(*_args, **_kwargs):
            response = MagicMock()
            response.json.return_value = mock_response
            response.raise_for_status.return_value = None
            return response

        mock_client_instance = AsyncMock()
        mock_client_instance.post.side_effect = mock_post
        mock_client_instance.get.side_effect = mock_get
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        # Clear cache
        service.cache.clear()

        crawl_request = CrawlRequest(
            urls=["https://example.com"],
            scrape_internal_links=True,
            follow_internal_links=True,
            max_depth=2,
            max_pages=10,
            cache_mode="disabled",
        )

        _result = await service.crawl_urls(crawl_request)

        # Check that only same-domain URLs were crawled
        assert any(
            "example.com" in url and url.count("/") <= 3 for url in crawled_urls
        )  # Seed URL
        assert any(
            "internal-page" in url or "same-domain" in url for url in crawled_urls
        )
        assert not any("different.com" in url for url in crawled_urls)
        assert not any("google.com" in url for url in crawled_urls)


@pytest.mark.asyncio
async def test_recursive_crawling_validation():
    """Test validation for recursive crawling parameters."""
    # Test that follow_internal_links requires scrape_internal_links
    with pytest.raises(
        ValueError, match="follow_internal_links requires scrape_internal_links"
    ):
        CrawlRequest(
            urls=["https://example.com"],
            scrape_internal_links=False,
            follow_internal_links=True,
        )

    # Test that follow_internal_links limits seed URLs to 3
    with pytest.raises(ValueError, match="maximum 3 seed URLs allowed"):
        CrawlRequest(
            urls=["https://a.com", "https://b.com", "https://c.com", "https://d.com"],
            scrape_internal_links=True,
            follow_internal_links=True,
        )


@pytest.mark.asyncio
async def test_recursive_crawling_with_cache():
    """Test that recursive crawling uses cache correctly."""
    service = CrawlingService()

    # Pre-populate cache with a result
    cached_data = {
        "url": "https://example.com/cached",
        "success": True,
        "markdown": "# Cached Page",
        "internal_links": ["/another-page"],
        "depth": 0,  # Will be overridden
    }
    service.cache.set(
        "https://example.com/cached",
        {
            "markdown_only": False,
            "scrape_internal_links": True,
            "scrape_external_links": False,
            "capture_screenshots": False,
            "follow_internal_links": True,
            "max_depth": 2,
            "max_pages": 10,
        },
        cached_data,
    )

    # Mock response for root page
    root_response = {
        "status": "completed",
        "results": [
            {
                "status_code": 200,
                "markdown": {"raw_markdown": "# Root Page"},
                "links": {"internal": [{"href": "/cached"}], "external": []},
            }
        ],
    }

    with patch("httpx.AsyncClient") as mock_client:
        mock_post_response = MagicMock()
        mock_post_response.json.return_value = {"task_id": "task-1"}
        mock_post_response.raise_for_status.return_value = None

        mock_get_response = MagicMock()
        mock_get_response.json.return_value = root_response
        mock_get_response.raise_for_status.return_value = None

        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_post_response
        mock_client_instance.get.return_value = mock_get_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        crawl_request = CrawlRequest(
            urls=["https://example.com"],
            scrape_internal_links=True,
            follow_internal_links=True,
            max_depth=2,
            max_pages=10,
        )

        result = await service.crawl_urls(crawl_request)

        # Should have one cached result
        assert result.cached_results == 1
        assert result.total_urls == 2  # Root + cached

        # Check that cached result has correct depth
        cached_result = next(r for r in result.results if "cached" in r.url)
        assert cached_result.depth == 1  # Should be depth 1 since discovered from root


@pytest.mark.asyncio
async def test_follow_external_links_basic():
    """Test basic external link following functionality."""
    service = CrawlingService()

    # Create responses for different domains
    def create_response_for_url(url):
        """Create appropriate response based on URL."""
        if "example.com" in url:
            # Root page with external links
            return {
                "status": "completed",
                "results": [
                    {
                        "status_code": 200,
                        "markdown": {"raw_markdown": "# Example.com Page"},
                        "links": {
                            "internal": [{"href": "/about"}],
                            "external": [
                                {"href": "https://httpbin.org"},
                                {"href": "https://different.com/page"},
                            ],
                        },
                    }
                ],
            }
        elif "httpbin.org" in url:
            # External page
            return {
                "status": "completed",
                "results": [
                    {
                        "status_code": 200,
                        "markdown": {"raw_markdown": "# HTTPBin Page"},
                        "links": {"internal": [], "external": []},
                    }
                ],
            }
        elif "different.com" in url:
            # Another external page
            return {
                "status": "completed",
                "results": [
                    {
                        "status_code": 200,
                        "markdown": {"raw_markdown": "# Different.com Page"},
                        "links": {"internal": [], "external": []},
                    }
                ],
            }
        else:
            return create_failed_task_response()

    call_count = 0

    with patch("httpx.AsyncClient") as mock_client:

        def mock_post(*_args, **_kwargs):
            nonlocal call_count
            call_count += 1
            response = MagicMock()
            response.json.return_value = {"task_id": f"task-{call_count}"}
            response.raise_for_status.return_value = None
            return response

        def mock_get(*_args, **_kwargs):
            url = _args[0] if _args else _kwargs.get("url", "")

            # Map task IDs to URLs
            if "task-1" in url:
                response_data = create_response_for_url("https://example.com")
            elif "task-2" in url:
                response_data = create_response_for_url("https://httpbin.org")
            elif "task-3" in url:
                response_data = create_response_for_url("https://different.com/page")
            else:
                response_data = create_failed_task_response()

            response = MagicMock()
            response.json.return_value = response_data
            response.raise_for_status.return_value = None
            return response

        mock_client_instance = AsyncMock()
        mock_client_instance.post.side_effect = mock_post
        mock_client_instance.get.side_effect = mock_get
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        # Clear cache
        service.cache.clear()

        crawl_request = CrawlRequest(
            urls=["https://example.com"],
            scrape_external_links=True,
            follow_external_links=True,
            max_depth=2,
            max_pages=5,
            cache_mode="disabled",
        )

        result = await service.crawl_urls(crawl_request)

        # Should have crawled the root page and external links
        assert result.total_urls == 3  # Root + 2 external
        assert result.successful_crawls == 3
        assert result.failed_crawls == 0

        # Check depth levels
        depths = {r.url: r.depth for r in result.results}
        assert depths["https://example.com"] == 0  # Seed URL (normalized)
        assert depths["https://httpbin.org"] == 1  # External link at depth 1
        assert depths["https://different.com/page"] == 1  # External link at depth 1


@pytest.mark.asyncio
async def test_follow_external_links_validation():
    """Test validation for external link following."""
    # Test that follow_external_links requires scrape_external_links
    with pytest.raises(
        ValueError, match="follow_external_links requires scrape_external_links"
    ):
        CrawlRequest(
            urls=["https://example.com"],
            scrape_external_links=False,
            follow_external_links=True,
        )


@pytest.mark.asyncio
async def test_follow_both_internal_and_external_links():
    """Test following both internal and external links."""
    service = CrawlingService()

    # Create a page with both internal and external links
    mock_response = {
        "status": "completed",
        "results": [
            {
                "status_code": 200,
                "markdown": {"raw_markdown": "# Mixed Links Page"},
                "links": {
                    "internal": [{"href": "/internal-page"}],
                    "external": [{"href": "https://external.com"}],
                },
            }
        ],
    }

    call_count = 0

    with patch("httpx.AsyncClient") as mock_client:

        def mock_post(*_args, **_kwargs):
            nonlocal call_count
            call_count += 1
            response = MagicMock()
            response.json.return_value = {"task_id": f"task-{call_count}"}
            response.raise_for_status.return_value = None
            return response

        def mock_get(*_args, **_kwargs):
            response = MagicMock()
            response.json.return_value = mock_response
            response.raise_for_status.return_value = None
            return response

        mock_client_instance = AsyncMock()
        mock_client_instance.post.side_effect = mock_post
        mock_client_instance.get.side_effect = mock_get
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        # Clear cache
        service.cache.clear()

        crawl_request = CrawlRequest(
            urls=["https://example.com"],
            scrape_internal_links=True,
            scrape_external_links=True,
            follow_internal_links=True,
            follow_external_links=True,
            max_depth=2,
            max_pages=5,
            cache_mode="disabled",
        )

        result = await service.crawl_urls(crawl_request)

        # Should have crawled root + internal + external
        assert result.total_urls == 3
        assert result.successful_crawls == 3

        # Check that we have URLs from different domains
        urls = [r.url for r in result.results]
        assert any("example.com" in url for url in urls)
        assert any("external.com" in url for url in urls)


@pytest.mark.asyncio
async def test_external_links_respect_max_pages():
    """Test that external link following respects max_pages limit."""
    service = CrawlingService()

    # Create a page with many external links
    mock_response = {
        "status": "completed",
        "results": [
            {
                "status_code": 200,
                "markdown": {"raw_markdown": "# Many External Links"},
                "links": {
                    "internal": [],
                    "external": [
                        {"href": f"https://external{i}.com"} for i in range(10)
                    ],
                },
            }
        ],
    }

    call_count = 0

    with patch("httpx.AsyncClient") as mock_client:

        def mock_post(*_args, **_kwargs):
            nonlocal call_count
            call_count += 1
            response = MagicMock()
            response.json.return_value = {"task_id": f"task-{call_count}"}
            response.raise_for_status.return_value = None
            return response

        def mock_get(*_args, **_kwargs):
            response = MagicMock()
            response.json.return_value = mock_response
            response.raise_for_status.return_value = None
            return response

        mock_client_instance = AsyncMock()
        mock_client_instance.post.side_effect = mock_post
        mock_client_instance.get.side_effect = mock_get
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        # Clear cache
        service.cache.clear()

        crawl_request = CrawlRequest(
            urls=["https://example.com"],
            scrape_external_links=True,
            follow_external_links=True,
            max_depth=2,
            max_pages=3,  # Limit to 3 pages total
            cache_mode="disabled",
        )

        result = await service.crawl_urls(crawl_request)

        # Should respect max_pages limit
        assert result.total_urls == 3
        assert len(result.results) == 3


@pytest.mark.asyncio
async def test_external_links_only_different_domains():
    """Test that external link following only follows links to different domains."""
    service = CrawlingService()

    # Track which URLs are crawled
    crawled_urls = []

    # Create a page with mixed links
    mock_response = {
        "status": "completed",
        "results": [
            {
                "status_code": 200,
                "markdown": {"raw_markdown": "# Mixed Domain Links"},
                "links": {
                    "internal": [{"href": "/same-domain"}],
                    "external": [
                        {
                            "href": "https://example.com/also-same"
                        },  # Same domain as seed
                        {"href": "https://different.com"},  # Different domain
                        {"href": "https://another.com"},  # Different domain
                    ],
                },
            }
        ],
    }

    with patch("httpx.AsyncClient") as mock_client:

        def mock_post(*_args, **_kwargs):
            payload = _kwargs.get("json", {})
            urls = payload.get("urls", [])
            if urls:
                crawled_urls.append(urls[0])

            response = MagicMock()
            response.json.return_value = {"task_id": f"task-{len(crawled_urls)}"}
            response.raise_for_status.return_value = None
            return response

        def mock_get(*_args, **_kwargs):
            response = MagicMock()
            response.json.return_value = mock_response
            response.raise_for_status.return_value = None
            return response

        mock_client_instance = AsyncMock()
        mock_client_instance.post.side_effect = mock_post
        mock_client_instance.get.side_effect = mock_get
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        # Clear cache
        service.cache.clear()

        crawl_request = CrawlRequest(
            urls=["https://example.com"],
            scrape_external_links=True,
            follow_external_links=True,
            max_depth=2,
            max_pages=5,
            cache_mode="disabled",
        )

        await service.crawl_urls(crawl_request)

        # Check that only different domains were crawled
        assert any("example.com" in url for url in crawled_urls)  # Seed URL
        assert any("different.com" in url for url in crawled_urls)  # External domain
        assert any("another.com" in url for url in crawled_urls)  # External domain
        # Should NOT crawl same-domain external links via external link following
        external_crawled = [url for url in crawled_urls if "example.com" not in url]
        assert all(
            "different.com" in url or "another.com" in url for url in external_crawled
        )


def test_external_links_safety_depth_limit():
    """Test that external link following has stricter depth limits."""
    import pytest

    from pydantic import ValidationError

    # Should reject depth > 3 for external links
    with pytest.raises(ValidationError, match="maximum depth is 3 for security"):
        CrawlRequest(
            urls=["https://example.com"],
            scrape_external_links=True,
            follow_external_links=True,
            max_depth=4,  # Too high for external links
        )

    # Should accept depth <= 3 for external links
    request = CrawlRequest(
        urls=["https://example.com"],
        scrape_external_links=True,
        follow_external_links=True,
        max_depth=3,  # Maximum allowed for external links
    )
    assert request.max_depth == 3


def test_external_links_safety_pages_limit():
    """Test that external link following has stricter page limits."""
    import pytest

    from pydantic import ValidationError

    # Should reject pages > 20 for external links
    with pytest.raises(ValidationError, match="maximum pages is 20 for security"):
        CrawlRequest(
            urls=["https://example.com"],
            scrape_external_links=True,
            follow_external_links=True,
            max_pages=25,  # Too high for external links
        )

    # Should accept pages <= 20 for external links
    request = CrawlRequest(
        urls=["https://example.com"],
        scrape_external_links=True,
        follow_external_links=True,
        max_pages=20,  # Maximum allowed for external links
    )
    assert request.max_pages == 20


def test_internal_links_can_use_full_limits():
    """Test that internal link following can use full limits (not restricted)."""
    # Should allow depth = 5 for internal links only
    request = CrawlRequest(
        urls=["https://example.com"],
        scrape_internal_links=True,
        follow_internal_links=True,
        max_depth=5,  # Maximum allowed
    )
    assert request.max_depth == 5

    # Should allow pages = 50 for internal links only
    request = CrawlRequest(
        urls=["https://example.com"],
        scrape_internal_links=True,
        follow_internal_links=True,
        max_pages=50,  # Maximum allowed
    )
    assert request.max_pages == 50


def test_url_normalization():
    """Test URL normalization for deduplication."""
    service = CrawlingService()

    # Test fragment removal
    assert (
        service._normalize_url("https://example.com/page#section1")
        == "https://example.com/page"
    )
    assert (
        service._normalize_url("https://example.com/page#section2")
        == "https://example.com/page"
    )

    # Test trailing slash removal
    assert (
        service._normalize_url("https://example.com/page/")
        == "https://example.com/page"
    )
    assert (
        service._normalize_url("https://example.com/page") == "https://example.com/page"
    )

    # Test root path normalization
    assert service._normalize_url("https://example.com/") == "https://example.com"
    assert service._normalize_url("https://example.com") == "https://example.com"

    # Test case normalization
    assert (
        service._normalize_url("HTTPS://EXAMPLE.COM/Page") == "https://example.com/Page"
    )

    # Test query parameter preservation
    assert (
        service._normalize_url("https://example.com/page?param=value#fragment")
        == "https://example.com/page?param=value"
    )

    # Test complex URL with all components
    complex_url = (
        "HTTPS://EXAMPLE.COM:443/Path/SubPath/?query=value&other=param#fragment"
    )
    expected = "https://example.com:443/Path/SubPath?query=value&other=param"
    assert service._normalize_url(complex_url) == expected


@pytest.mark.asyncio
async def test_url_deduplication_fragments():
    """Test that URLs with different fragments are treated as the same page."""
    service = CrawlingService()

    # Mock the Crawl4AI API responses
    task_completion_response = {
        "status": "completed",
        "results": [
            {
                "status_code": 200,
                "markdown": {"raw_markdown": "# Test Page"},
                "cleaned_html": "<h1>Test Page</h1>",
                "metadata": {"title": "Test"},
                "links": {
                    "internal": [
                        {"href": "/about#section1"},
                        {"href": "/about#section2"},  # Same page, different fragment
                        {"href": "/contact"},
                    ]
                },
            }
        ],
    }

    mock_client_instance = create_async_api_mocks(task_completion_response)

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        crawl_request = CrawlRequest(
            urls=["https://example.com"],
            scrape_internal_links=True,
            follow_internal_links=True,
            max_depth=2,
            max_pages=10,
            cache_mode="disabled",
        )

        await service.crawl_urls(crawl_request)

        # Count how many times each normalized URL appears in crawl calls
        # Extract URLs from JSON payloads in POST calls
        crawl_calls = []
        for call in mock_client_instance.post.call_args_list:
            if call.kwargs and "json" in call.kwargs:
                json_payload = call.kwargs["json"]
                if json_payload.get("urls"):
                    crawl_calls.append(json_payload["urls"][0])

        # Should only crawl each unique page once, even though fragments differ
        unique_pages = {service._normalize_url(url) for url in crawl_calls}

        # Should have crawled:
        # 1. https://example.com (seed, normalized)
        # 2. https://example.com/about (only once, despite two different fragments)
        # 3. https://example.com/contact
        assert len(unique_pages) == 3
        assert "https://example.com" in unique_pages  # Root URL normalized
        assert "https://example.com/about" in unique_pages  # Normalized, no fragment
        assert "https://example.com/contact" in unique_pages


@pytest.mark.asyncio
async def test_url_deduplication_trailing_slash():
    """Test that URLs with and without trailing slashes are treated as the same page."""
    service = CrawlingService()

    # Mock response with links that have trailing slash variations
    task_completion_response = {
        "status": "completed",
        "results": [
            {
                "status_code": 200,
                "markdown": {"raw_markdown": "# Test Page"},
                "cleaned_html": "<h1>Test Page</h1>",
                "metadata": {"title": "Test"},
                "links": {
                    "internal": [
                        {"href": "/about/"},  # With trailing slash
                        {"href": "/about"},  # Without trailing slash (same page)
                        {"href": "/contact/"},
                    ]
                },
            }
        ],
    }

    mock_client_instance = create_async_api_mocks(task_completion_response)

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        crawl_request = CrawlRequest(
            urls=["https://example.com"],
            scrape_internal_links=True,
            follow_internal_links=True,
            max_depth=2,
            max_pages=10,
            cache_mode="disabled",
        )

        await service.crawl_urls(crawl_request)

        # Count how many times each normalized URL appears in crawl calls
        # Extract URLs from JSON payloads in POST calls
        crawl_calls = []
        for call in mock_client_instance.post.call_args_list:
            if call.kwargs and "json" in call.kwargs:
                json_payload = call.kwargs["json"]
                if json_payload.get("urls"):
                    crawl_calls.append(json_payload["urls"][0])

        unique_pages = {service._normalize_url(url) for url in crawl_calls}

        # Should have crawled:
        # 1. https://example.com (seed, normalized)
        # 2. https://example.com/about (only once, despite trailing slash variation)
        # 3. https://example.com/contact
        assert len(unique_pages) == 3
        assert "https://example.com" in unique_pages  # Root URL normalized
        assert (
            "https://example.com/about" in unique_pages
        )  # Normalized, no trailing slash
        assert "https://example.com/contact" in unique_pages


@pytest.mark.asyncio
async def test_url_deduplication_case_insensitive_domain():
    """Test that domain names are normalized case-insensitively."""
    service = CrawlingService()

    # Mock response with links that have different case domains
    task_completion_response = {
        "status": "completed",
        "results": [
            {
                "status_code": 200,
                "markdown": {"raw_markdown": "# Test Page"},
                "cleaned_html": "<h1>Test Page</h1>",
                "metadata": {"title": "Test"},
                "links": {
                    "external": [
                        {"href": "https://EXTERNAL.COM/page"},  # Uppercase domain
                        {
                            "href": "https://external.com/page"
                        },  # Lowercase domain (same)
                        {"href": "https://other.com/page"},  # Different domain
                    ]
                },
            }
        ],
    }

    mock_client_instance = create_async_api_mocks(task_completion_response)

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        crawl_request = CrawlRequest(
            urls=["https://example.com"],
            scrape_external_links=True,
            follow_external_links=True,
            max_depth=2,
            max_pages=10,
            cache_mode="disabled",
        )

        await service.crawl_urls(crawl_request)

        # Count how many times each normalized URL appears in crawl calls
        # Extract URLs from JSON payloads in POST calls
        crawl_calls = []
        for call in mock_client_instance.post.call_args_list:
            if call.kwargs and "json" in call.kwargs:
                json_payload = call.kwargs["json"]
                if json_payload.get("urls"):
                    crawl_calls.append(json_payload["urls"][0])

        unique_pages = {service._normalize_url(url) for url in crawl_calls}

        # Should have crawled:
        # 1. https://example.com (seed, normalized)
        # 2. https://external.com/page (only once, despite case variation)
        # 3. https://other.com/page
        assert len(unique_pages) == 3
        assert "https://example.com" in unique_pages  # Root URL normalized
        assert "https://external.com/page" in unique_pages  # Normalized to lowercase
        assert "https://other.com/page" in unique_pages

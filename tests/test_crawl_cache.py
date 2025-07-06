from datetime import datetime, timedelta

from services.crawl_cache import CrawlingCache


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
    options3 = {
        "markdown_only": True,
        "capture_screenshots": True,
        "screenshot_width": 1280,
        "screenshot_height": 720,
    }
    test_data = {"url": url, "success": True}

    cache.set(url, options1, test_data)

    # Different options should not hit cache
    assert cache.get(url, options2) is None
    assert cache.get(url, options3) is None
    # Same options should hit cache
    assert cache.get(url, options1) == test_data


def test_cache_key_considers_screenshot_options():
    """Test that cache keys include screenshot-specific options."""
    cache = CrawlingCache(ttl_hours=1)

    url = "https://example.com"
    base_options = {"markdown_only": False, "capture_screenshots": True}

    # Different screenshot dimensions should create different cache keys
    options1 = {**base_options, "screenshot_width": 1920, "screenshot_height": 1080}
    options2 = {**base_options, "screenshot_width": 1280, "screenshot_height": 720}
    options3 = {**base_options, "screenshot_wait_for": 5}

    test_data = {"url": url, "success": True}

    cache.set(url, options1, test_data)

    # Different screenshot options should not hit cache
    assert cache.get(url, options2) is None
    assert cache.get(url, options3) is None
    # Same options should hit cache
    assert cache.get(url, options1) == test_data


def test_cache_key_considers_link_options():
    """Test that cache keys include link extraction options."""
    cache = CrawlingCache(ttl_hours=1)

    url = "https://example.com"

    options1 = {"scrape_internal_links": True, "scrape_external_links": False}
    options2 = {"scrape_internal_links": False, "scrape_external_links": True}
    options3 = {"scrape_internal_links": True, "scrape_external_links": True}

    test_data = {"url": url, "success": True}

    cache.set(url, options1, test_data)

    # Different link options should not hit cache
    assert cache.get(url, options2) is None
    assert cache.get(url, options3) is None
    # Same options should hit cache
    assert cache.get(url, options1) == test_data


def test_cache_url_normalization():
    """Test that URLs are normalized for caching."""
    cache = CrawlingCache(ttl_hours=1)

    options = {"markdown_only": True}
    test_data = {"url": "https://example.com", "success": True}

    # Set with one URL format
    cache.set("https://EXAMPLE.com", options, test_data)

    # Should find with normalized URL
    result = cache.get("https://example.com", options)
    assert result == test_data

    # Should also work with whitespace
    cache.set(" https://test.com ", options, test_data)
    result = cache.get("https://test.com", options)
    assert result == test_data


def test_cache_expiry():
    """Test that expired entries are removed."""
    cache = CrawlingCache(ttl_hours=1)

    url = "https://example.com"
    options = {"markdown_only": True}
    test_data = {"url": url, "success": True}

    cache.set(url, options, test_data)

    # Manually expire the entry
    key = cache._get_key(url, options)
    old_time = datetime.now() - timedelta(hours=2)
    cache._cache[key] = (cache._cache[key][0], old_time)

    result = cache.get(url, options)
    assert result is None
    # Check that expired entry was removed
    assert key not in cache._cache


def test_cache_miss_returns_none():
    """Test that cache miss returns None."""
    cache = CrawlingCache(ttl_hours=1)

    result = cache.get("https://nonexistent.com", {"markdown_only": True})
    assert result is None


def test_cache_overwrite():
    """Test that cache entries can be overwritten."""
    cache = CrawlingCache(ttl_hours=1)

    url = "https://example.com"
    options = {"markdown_only": True}

    # Set initial data
    initial_data = {"url": url, "success": True, "markdown": "# Initial"}
    cache.set(url, options, initial_data)

    # Overwrite with new data
    new_data = {"url": url, "success": True, "markdown": "# Updated"}
    cache.set(url, options, new_data)

    result = cache.get(url, options)
    assert result == new_data


def test_cache_multiple_urls():
    """Test cache with multiple URLs and different options."""
    cache = CrawlingCache(ttl_hours=1)

    test_cases = [
        (
            "https://example.com",
            {"markdown_only": True},
            {"url": "https://example.com", "success": True},
        ),
        (
            "https://test.com",
            {"scrape_internal_links": True},
            {"url": "https://test.com", "success": True},
        ),
        (
            "https://demo.com",
            {"capture_screenshots": True, "screenshot_width": 1920},
            {"url": "https://demo.com", "success": True},
        ),
    ]

    # Store all entries
    for url, options, data in test_cases:
        cache.set(url, options, data)

    # Retrieve all entries
    for url, options, expected_data in test_cases:
        result = cache.get(url, options)
        assert result == expected_data


def test_cache_size_tracking():
    """Test cache size tracking."""
    cache = CrawlingCache(ttl_hours=1)

    assert cache.size() == 0

    # Add entries
    cache.set("https://example.com", {"markdown_only": True}, {"success": True})
    assert cache.size() == 1

    cache.set("https://test.com", {"markdown_only": False}, {"success": True})
    assert cache.size() == 2

    # Same URL with same options should not increase size
    cache.set("https://example.com", {"markdown_only": True}, {"success": True})
    assert cache.size() == 2

    # Same URL with different options should increase size
    cache.set("https://example.com", {"markdown_only": False}, {"success": True})
    assert cache.size() == 3


def test_cache_clear():
    """Test cache clearing functionality."""
    cache = CrawlingCache(ttl_hours=1)

    # Add some entries
    cache.set("https://example.com", {"markdown_only": True}, {"success": True})
    cache.set("https://test.com", {"markdown_only": False}, {"success": True})

    assert cache.size() == 2

    # Clear cache
    cache.clear()
    assert cache.size() == 0

    # Entries should no longer be retrievable
    assert cache.get("https://example.com", {"markdown_only": True}) is None
    assert cache.get("https://test.com", {"markdown_only": False}) is None


def test_cache_cleanup_expired():
    """Test cleanup of expired entries."""
    cache = CrawlingCache(ttl_hours=1)

    # Add valid entry
    cache.set("https://valid.com", {"markdown_only": True}, {"success": True})

    # Add entry that we'll manually expire
    cache.set("https://expired.com", {"markdown_only": True}, {"success": True})
    expired_key = cache._get_key("https://expired.com", {"markdown_only": True})
    old_time = datetime.now() - timedelta(hours=2)
    cache._cache[expired_key] = (cache._cache[expired_key][0], old_time)

    assert cache.size() == 2

    # Cleanup expired entries
    expired_count = cache.cleanup_expired()
    assert expired_count == 1
    assert cache.size() == 1

    # Valid entry should still be there
    assert cache.get("https://valid.com", {"markdown_only": True}) is not None
    # Expired entry should be gone
    assert cache.get("https://expired.com", {"markdown_only": True}) is None


def test_cache_ttl_configuration():
    """Test cache with different TTL configurations."""
    # Short TTL
    cache_short = CrawlingCache(ttl_hours=1)
    assert cache_short.ttl == timedelta(hours=1)

    # Long TTL
    cache_long = CrawlingCache(ttl_hours=24)
    assert cache_long.ttl == timedelta(hours=24)


def test_cache_key_generation_consistency():
    """Test that cache key generation is consistent and deterministic."""
    cache = CrawlingCache(ttl_hours=1)

    url = "https://example.com"
    options = {
        "markdown_only": True,
        "scrape_internal_links": False,
        "scrape_external_links": True,
        "capture_screenshots": True,
        "screenshot_width": 1920,
        "screenshot_height": 1080,
        "screenshot_wait_for": 2,
    }

    # Same URL and options should generate same key
    key1 = cache._get_key(url, options)
    key2 = cache._get_key(url, options)
    assert key1 == key2

    # Different URL should generate different key
    key3 = cache._get_key("https://different.com", options)
    assert key1 != key3

    # Different options should generate different key
    different_options = {**options, "markdown_only": False}
    key4 = cache._get_key(url, different_options)
    assert key1 != key4


def test_cache_options_with_all_screenshot_parameters():
    """Test cache with all screenshot parameters."""
    cache = CrawlingCache(ttl_hours=1)

    url = "https://example.com"
    options = {
        "markdown_only": False,
        "scrape_internal_links": True,
        "scrape_external_links": True,
        "capture_screenshots": True,
        "screenshot_width": 1280,
        "screenshot_height": 720,
        "screenshot_wait_for": 5,
    }

    test_data = {
        "url": url,
        "success": True,
        "markdown": "# Test",
        "screenshot_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
    }

    cache.set(url, options, test_data)
    result = cache.get(url, options)

    assert result == test_data

    # Slightly different options should not hit cache
    modified_options = {**options, "screenshot_width": 1920}
    assert cache.get(url, modified_options) is None

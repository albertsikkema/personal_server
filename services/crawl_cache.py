"""
Caching service for crawling operations.

This module provides in-memory caching for crawling results with TTL support.
Cache keys include all crawling options to ensure proper cache isolation.
"""

import hashlib
import json
from datetime import datetime, timedelta
from typing import Any

from config import settings


class CrawlingCache:
    """
    In-memory cache for crawling results with TTL support.

    Cache keys are generated from URL + all crawling options to ensure
    different configurations don't interfere with each other.
    """

    def __init__(self, ttl_hours: int | None = None):
        """
        Initialize the crawling cache.

        Args:
            ttl_hours: Time-to-live in hours (defaults to config setting)
        """
        self.ttl = timedelta(hours=ttl_hours or settings.CRAWLING_CACHE_TTL_HOURS)
        self._cache: dict[str, tuple[dict[str, Any], datetime]] = {}
        # Reverse lookup: normalized_url -> set of cache keys
        self._url_to_keys: dict[str, set[str]] = {}

    def _normalize_url(self, url: str) -> str:
        """
        Normalize URL for consistent caching.

        Args:
            url: Raw URL string

        Returns:
            Normalized URL string
        """
        # Convert to string if it's an HttpUrl object
        url_str = str(url)

        # Basic normalization: strip whitespace, convert to lowercase
        url_str = url_str.strip().lower()

        # Remove trailing slash for consistency (except for root URLs)
        if url_str.endswith("/") and url_str.count("/") > 2:
            url_str = url_str.rstrip("/")
        elif url_str.endswith("/") and url_str.count("/") == 3:
            # Handle cases like https://example.com/
            url_str = url_str.rstrip("/")

        return url_str

    def _get_key(self, url: str, options: dict[str, Any]) -> str:
        """
        Generate cache key from URL and crawling options.

        Cache keys must include all relevant options to prevent
        cache collisions between different crawling configurations.

        Args:
            url: The URL to crawl
            options: Crawling options dictionary

        Returns:
            MD5 hash of normalized URL + options
        """
        normalized_url = self._normalize_url(url)

        # Create a deterministic representation of crawling options
        # Only include options that affect the crawling result
        cache_relevant_options = {
            "markdown_only": options.get("markdown_only", False),
            "scrape_internal_links": options.get("scrape_internal_links", False),
            "scrape_external_links": options.get("scrape_external_links", False),
            "capture_screenshots": options.get("capture_screenshots", False),
        }

        # Include screenshot-specific options if screenshots are enabled
        if cache_relevant_options["capture_screenshots"]:
            cache_relevant_options.update(
                {
                    "screenshot_width": options.get("screenshot_width", 1920),
                    "screenshot_height": options.get("screenshot_height", 1080),
                    "screenshot_wait_for": options.get("screenshot_wait_for", 2),
                }
            )

        # Create cache key data structure
        cache_data = {"url": normalized_url, "options": cache_relevant_options}

        # Generate deterministic hash
        cache_string = json.dumps(cache_data, sort_keys=True, separators=(",", ":"))
        return hashlib.md5(cache_string.encode()).hexdigest()

    def get(self, url: str, options: dict[str, Any]) -> dict[str, Any] | None:
        """
        Retrieve cached crawling result.

        Args:
            url: The URL that was crawled
            options: Crawling options used

        Returns:
            Cached result dictionary or None if not found/expired
        """
        key = self._get_key(url, options)

        if key not in self._cache:
            return None

        data, timestamp = self._cache[key]

        # Check if entry has expired
        if datetime.now() - timestamp > self.ttl:
            # Remove expired entry
            del self._cache[key]
            return None

        return data

    def set(self, url: str, options: dict[str, Any], data: dict[str, Any]) -> None:
        """
        Store crawling result in cache.

        Args:
            url: The URL that was crawled
            options: Crawling options used
            data: Result data to cache
        """
        key = self._get_key(url, options)
        normalized_url = self._normalize_url(url)

        # Store in main cache
        self._cache[key] = (data, datetime.now())

        # Update reverse lookup
        if normalized_url not in self._url_to_keys:
            self._url_to_keys[normalized_url] = set()
        self._url_to_keys[normalized_url].add(key)

    def size(self) -> int:
        """
        Get current cache size.

        Returns:
            Number of cached entries
        """
        return len(self._cache)

    def clear(self) -> int:
        """
        Clear all cached entries.

        Returns:
            Number of entries that were cleared
        """
        count = len(self._cache)
        self._cache.clear()
        self._url_to_keys.clear()
        return count

    def cleanup_expired(self) -> int:
        """
        Remove expired entries from cache.

        Returns:
            Number of expired entries removed
        """
        current_time = datetime.now()
        expired_keys = []

        for key, (_, timestamp) in self._cache.items():
            if current_time - timestamp > self.ttl:
                expired_keys.append(key)

        # Remove expired keys from both caches
        for key in expired_keys:
            del self._cache[key]

        # Clean up reverse lookup entries
        self._cleanup_reverse_lookup(expired_keys)

        return len(expired_keys)

    def _cleanup_reverse_lookup(self, removed_keys: list[str]) -> None:
        """
        Clean up reverse lookup entries for removed keys.

        Args:
            removed_keys: List of cache keys that were removed
        """
        # Remove keys from URL reverse lookup
        urls_to_remove = []
        for url, keys in self._url_to_keys.items():
            keys.difference_update(removed_keys)
            if not keys:  # If no keys left for this URL
                urls_to_remove.append(url)

        # Remove empty URL entries
        for url in urls_to_remove:
            del self._url_to_keys[url]

    def get_stats(self) -> dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache statistics
        """
        return {
            "cache_size": self.size(),
            "cache_ttl_hours": self.ttl.total_seconds() / 3600,
            "oldest_entry_age_minutes": self._get_oldest_entry_age(),
            "expired_entries": self._count_expired_entries(),
        }

    def _get_oldest_entry_age(self) -> float | None:
        """
        Get age of oldest cache entry in minutes.

        Returns:
            Age in minutes or None if cache is empty
        """
        if not self._cache:
            return None

        current_time = datetime.now()
        oldest_timestamp = min(timestamp for _, timestamp in self._cache.values())
        age_delta = current_time - oldest_timestamp
        return age_delta.total_seconds() / 60

    def _count_expired_entries(self) -> int:
        """
        Count number of expired entries (without removing them).

        Returns:
            Number of expired entries
        """
        current_time = datetime.now()
        expired_count = 0

        for _, (_, timestamp) in self._cache.items():
            if current_time - timestamp > self.ttl:
                expired_count += 1

        return expired_count

    def has_cached_result(self, url: str, options: dict[str, Any]) -> bool:
        """
        Check if a valid cached result exists without retrieving it.

        Args:
            url: The URL to check
            options: Crawling options

        Returns:
            True if valid cached result exists
        """
        key = self._get_key(url, options)

        if key not in self._cache:
            return False

        _, timestamp = self._cache[key]
        return datetime.now() - timestamp <= self.ttl

    def invalidate_url(self, url: str) -> int:
        """
        Invalidate all cached entries for a specific URL.

        This removes all cached results for the URL regardless of options.
        Useful when you know a page has changed.

        Args:
            url: URL to invalidate

        Returns:
            Number of entries invalidated
        """
        normalized_url = self._normalize_url(url)

        # Use reverse lookup for efficient invalidation
        if normalized_url not in self._url_to_keys:
            return 0

        keys_to_remove = list(self._url_to_keys[normalized_url])

        # Remove from main cache
        for key in keys_to_remove:
            if key in self._cache:
                del self._cache[key]

        # Remove from reverse lookup
        del self._url_to_keys[normalized_url]

        return len(keys_to_remove)

    def get_cache_key_preview(
        self, url: str, options: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Get a preview of how cache key is generated (for debugging).

        Args:
            url: URL to preview
            options: Crawling options

        Returns:
            Dictionary with key generation details
        """
        normalized_url = self._normalize_url(url)
        key = self._get_key(url, options)

        # Extract relevant options
        cache_relevant_options = {
            "markdown_only": options.get("markdown_only", False),
            "scrape_internal_links": options.get("scrape_internal_links", False),
            "scrape_external_links": options.get("scrape_external_links", False),
            "capture_screenshots": options.get("capture_screenshots", False),
        }

        if cache_relevant_options["capture_screenshots"]:
            cache_relevant_options.update(
                {
                    "screenshot_width": options.get("screenshot_width", 1920),
                    "screenshot_height": options.get("screenshot_height", 1080),
                    "screenshot_wait_for": options.get("screenshot_wait_for", 2),
                }
            )

        return {
            "cache_key": key,
            "normalized_url": normalized_url,
            "cache_relevant_options": cache_relevant_options,
            "full_cache_data": {
                "url": normalized_url,
                "options": cache_relevant_options,
            },
        }

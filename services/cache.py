"""
In-memory caching service for geocoding results.

This module provides caching functionality to reduce API calls to the Nominatim
service. Cache keys are normalized (case-insensitive, whitespace-trimmed) and
entries automatically expire after the configured TTL.

The cache helps comply with Nominatim's usage policy by minimizing unnecessary
API requests for recently queried cities.
"""

import hashlib
from datetime import datetime, timedelta
from typing import Optional

from utils.logging import get_logger

logger = get_logger(__name__)


class GeocodingCache:
    """
    In-memory cache for geocoding results to minimize API calls.

    Provides thread-safe caching with automatic expiration based on TTL.
    Cache keys are normalized to be case-insensitive and whitespace-trimmed
    for consistent lookup behavior.

    Args:
        ttl_hours: Time-to-live for cache entries in hours
    """

    def __init__(self, ttl_hours: int = 24):
        """
        Initialize the geocoding cache.

        Args:
            ttl_hours: Time-to-live for cache entries in hours (default: 24)
        """
        self._cache: dict[str, tuple[dict, datetime]] = {}
        self.ttl = timedelta(hours=ttl_hours)

        logger.debug(f"GeocodingCache initialized with TTL: {ttl_hours} hours")

    def _get_key(self, city: str) -> str:
        """
        Generate cache key from city name.

        Normalizes the city name by converting to lowercase and removing
        leading/trailing whitespace, then generates an MD5 hash for
        consistent key format.

        Args:
            city: City name to generate key for

        Returns:
            MD5 hash of normalized city name
        """
        normalized = city.lower().strip()
        return hashlib.md5(normalized.encode()).hexdigest()

    def get(self, city: str) -> Optional[dict]:
        """
        Get cached result if exists and not expired.

        Args:
            city: City name to look up in cache

        Returns:
            Cached geocoding result dict if found and valid, None otherwise
        """
        key = self._get_key(city)
        if key in self._cache:
            data, timestamp = self._cache[key]
            if datetime.now() - timestamp < self.ttl:
                logger.info(f"Cache hit for city: {city}")
                return data
            else:
                # Remove expired entry
                del self._cache[key]
                logger.debug(f"Cache expired for city: {city}")

        logger.debug(f"Cache miss for city: {city}")
        return None

    def set(self, city: str, data: dict):
        """
        Cache a geocoding result.

        Args:
            city: City name to cache result for
            data: Geocoding result data to cache
        """
        key = self._get_key(city)
        self._cache[key] = (data, datetime.now())
        logger.debug(f"Cached result for city: {city} (cache size: {len(self._cache)})")

    def clear(self):
        """
        Clear all cached entries.

        Useful for testing or cache management.
        """
        self._cache.clear()
        logger.info("Cache cleared")

    def size(self) -> int:
        """
        Get current cache size.

        Returns:
            Number of entries currently in cache
        """
        return len(self._cache)

    def cleanup_expired(self):
        """
        Remove all expired entries from cache.

        This method can be called periodically to prevent memory bloat
        from expired entries that haven't been accessed.
        """
        current_time = datetime.now()
        expired_keys = []

        for key, (_data, timestamp) in self._cache.items():
            if current_time - timestamp >= self.ttl:
                expired_keys.append(key)

        for key in expired_keys:
            del self._cache[key]

        if expired_keys:
            logger.debug(f"Cleaned up {len(expired_keys)} expired cache entries")

        return len(expired_keys)

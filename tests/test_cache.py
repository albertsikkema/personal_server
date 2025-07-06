from datetime import datetime, timedelta

from services.cache import GeocodingCache


def test_cache_stores_and_retrieves():
    """Test basic cache functionality."""
    cache = GeocodingCache(ttl_hours=1)

    test_data = {"lat": 52.5, "lon": 13.4}
    cache.set("Berlin", test_data)

    result = cache.get("Berlin")
    assert result == test_data


def test_cache_case_insensitive():
    """Test that cache keys are case-insensitive."""
    cache = GeocodingCache(ttl_hours=1)

    test_data = {"lat": 52.5, "lon": 13.4}
    cache.set("Berlin", test_data)

    # Should find with different case
    result = cache.get("berlin")
    assert result == test_data

    result = cache.get("BERLIN")
    assert result == test_data

    result = cache.get("BeRlIn")
    assert result == test_data


def test_cache_whitespace_normalization():
    """Test that cache handles whitespace properly."""
    cache = GeocodingCache(ttl_hours=1)

    test_data = {"lat": 52.5, "lon": 13.4}
    cache.set(" Berlin ", test_data)

    # Should find with different whitespace
    result = cache.get("Berlin")
    assert result == test_data

    result = cache.get("  Berlin  ")
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
    # Check that expired entry was removed
    assert key not in cache._cache


def test_cache_miss_returns_none():
    """Test that cache miss returns None."""
    cache = GeocodingCache(ttl_hours=1)

    result = cache.get("NonExistentCity")
    assert result is None


def test_cache_overwrite():
    """Test that cache entries can be overwritten."""
    cache = GeocodingCache(ttl_hours=1)

    # Set initial data
    cache.set("Berlin", {"lat": 52.5, "lon": 13.4})

    # Overwrite with new data
    new_data = {"lat": 52.6, "lon": 13.5}
    cache.set("Berlin", new_data)

    result = cache.get("Berlin")
    assert result == new_data


def test_cache_multiple_entries():
    """Test cache with multiple entries."""
    cache = GeocodingCache(ttl_hours=1)

    cities = {
        "Berlin": {"lat": 52.5, "lon": 13.4},
        "London": {"lat": 51.5, "lon": -0.1},
        "Paris": {"lat": 48.9, "lon": 2.3},
    }

    # Store all cities
    for city, data in cities.items():
        cache.set(city, data)

    # Retrieve all cities
    for city, expected_data in cities.items():
        result = cache.get(city)
        assert result == expected_data


def test_cache_key_generation():
    """Test that cache key generation is consistent."""
    cache = GeocodingCache(ttl_hours=1)

    # Same city should generate same key
    key1 = cache._get_key("Berlin")
    key2 = cache._get_key("Berlin")
    assert key1 == key2

    # Case-insensitive
    key3 = cache._get_key("berlin")
    assert key1 == key3

    # Whitespace normalized
    key4 = cache._get_key(" Berlin ")
    assert key1 == key4

    # Different cities should generate different keys
    key_london = cache._get_key("London")
    assert key1 != key_london


def test_cache_ttl_configuration():
    """Test cache with different TTL configurations."""
    # Short TTL
    cache_short = GeocodingCache(ttl_hours=1)
    assert cache_short.ttl == timedelta(hours=1)

    # Long TTL
    cache_long = GeocodingCache(ttl_hours=48)
    assert cache_long.ttl == timedelta(hours=48)


def test_cache_empty_string_handling():
    """Test cache behavior with edge cases."""
    cache = GeocodingCache(ttl_hours=1)

    # Empty string should still work
    cache.set("", {"lat": 0, "lon": 0})
    result = cache.get("")
    assert result == {"lat": 0, "lon": 0}

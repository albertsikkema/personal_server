import asyncio
import time

import pytest

from services.rate_limiter import RateLimiter


@pytest.mark.asyncio
async def test_rate_limiter_allows_first_request():
    """Test that first request is allowed immediately."""
    limiter = RateLimiter(max_requests=1, time_window=1.0)

    start_time = time.time()
    await limiter.acquire()
    elapsed = time.time() - start_time

    assert elapsed < 0.1  # Should be nearly instant


@pytest.mark.asyncio
async def test_rate_limiter_enforces_delay():
    """Test that second request is delayed appropriately."""
    limiter = RateLimiter(max_requests=1, time_window=1.0)

    # First request
    await limiter.acquire()

    # Second request should be delayed
    start_time = time.time()
    await limiter.acquire()
    elapsed = time.time() - start_time

    assert elapsed >= 0.9  # Should wait close to 1 second


@pytest.mark.asyncio
async def test_rate_limiter_concurrent_requests():
    """Test that concurrent requests are properly serialized."""
    limiter = RateLimiter(max_requests=1, time_window=1.0)

    async def make_request():
        start_time = time.time()
        await limiter.acquire()
        return time.time() - start_time

    # Make 3 concurrent requests
    start_time = time.time()
    tasks = [make_request() for _ in range(3)]
    delays = await asyncio.gather(*tasks)
    total_elapsed = time.time() - start_time

    # First request should be immediate, others delayed
    assert delays[0] < 0.1  # First is immediate
    assert total_elapsed >= 2.0  # Total should be at least 2 seconds


@pytest.mark.asyncio
async def test_rate_limiter_thread_safety():
    """Test that rate limiter is thread-safe with asyncio."""
    limiter = RateLimiter(max_requests=1, time_window=0.5)

    request_times = []

    async def timed_request():
        await limiter.acquire()
        request_times.append(time.time())

    # Make multiple concurrent requests
    tasks = [timed_request() for _ in range(3)]
    await asyncio.gather(*tasks)

    # Check that requests were spaced appropriately
    assert len(request_times) == 3
    for i in range(1, len(request_times)):
        time_diff = request_times[i] - request_times[i - 1]
        assert time_diff >= 0.4  # Should be at least close to time_window


@pytest.mark.asyncio
async def test_rate_limiter_custom_params():
    """Test rate limiter with custom parameters."""
    limiter = RateLimiter(max_requests=1, time_window=0.2)

    # First request
    await limiter.acquire()

    # Second request should be delayed by 0.2 seconds
    start_time = time.time()
    await limiter.acquire()
    elapsed = time.time() - start_time

    assert elapsed >= 0.18  # Allow small margin for timing
    assert elapsed < 0.3  # But not too much delay

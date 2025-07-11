"""
Rate limiting service for Nominatim API compliance.

This module implements rate limiting to ensure compliance with Nominatim's
usage policy of maximum 1 request per second. The rate limiter uses async
locks to ensure thread safety in concurrent environments.

CRITICAL: Nominatim policy requires max 1 request per second to prevent IP bans.
"""

import asyncio
import time

from utils.logging import get_logger

logger = get_logger(__name__)


class RateLimiter:
    """
    Rate limiter to ensure Nominatim API limits are respected.

    Implements a token bucket-style rate limiter that ensures no more than
    max_requests are made within the specified time_window.

    Args:
        max_requests: Maximum number of requests allowed in time window
        time_window: Time window in seconds for rate limiting
    """

    def __init__(self, max_requests: int = 1, time_window: float = 1.0):
        """
        Initialize the rate limiter.

        Args:
            max_requests: Maximum requests allowed in time window (default: 1)
            time_window: Time window in seconds (default: 1.0)
        """
        self.max_requests = max_requests
        self.time_window = time_window  # in seconds
        self.last_request_time: float | None = None
        self._lock = asyncio.Lock()

        logger.debug(
            f"RateLimiter initialized: {max_requests} requests per {time_window}s"
        )

    async def acquire(self):
        """
        Ensure rate limit is not exceeded. Blocks if necessary.

        This method will sleep if calling it would exceed the rate limit,
        ensuring that the Nominatim 1 req/sec policy is never violated.

        Returns:
            None: Method completes when it's safe to make a request
        """
        async with self._lock:
            current_time = time.time()

            if self.last_request_time is not None:
                time_since_last = current_time - self.last_request_time
                if time_since_last < self.time_window:
                    sleep_time = self.time_window - time_since_last
                    logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f}s")
                    await asyncio.sleep(sleep_time)

            self.last_request_time = time.time()
            logger.debug("Rate limiter acquired - request allowed")

from unittest.mock import patch

import pytest

from config import settings
from dependencies import AuthHTTPException, optional_api_key, verify_api_key
from fastapi import status


class TestAuthenticationDependencies:
    """Test cases for authentication dependency functions."""

    def test_auth_http_exception_format(self):
        """Test that AuthHTTPException creates properly formatted responses."""
        message = "Test error"
        exc = AuthHTTPException(status.HTTP_401_UNAUTHORIZED, message)

        assert exc.response_content["detail"] == message
        assert "request_id" in exc.response_content
        assert "timestamp" in exc.response_content
        # Verify UUID format (36 characters with hyphens)
        assert len(exc.response_content["request_id"]) == 36
        assert exc.response_content["request_id"].count("-") == 4

    @pytest.mark.asyncio
    async def test_verify_api_key_valid(self):
        """Test that verify_api_key succeeds with valid API key."""
        valid_key = settings.API_KEY

        with patch("dependencies.logger"):
            result = await verify_api_key(valid_key)
            assert result == valid_key

    @pytest.mark.asyncio
    async def test_verify_api_key_missing(self):
        """Test that verify_api_key fails with missing API key."""
        with patch("dependencies.logger"):
            with pytest.raises(AuthHTTPException) as exc_info:
                await verify_api_key(None)

            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            content = exc_info.value.response_content
            assert content["detail"] == "API key missing"
            assert "request_id" in content
            assert "timestamp" in content

    @pytest.mark.asyncio
    async def test_verify_api_key_invalid(self):
        """Test that verify_api_key fails with invalid API key."""
        invalid_key = "invalid-key"

        with patch("dependencies.logger"):
            with pytest.raises(AuthHTTPException) as exc_info:
                await verify_api_key(invalid_key)

            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            content = exc_info.value.response_content
            assert content["detail"] == "Invalid API key"
            assert "request_id" in content
            assert "timestamp" in content

    @pytest.mark.asyncio
    async def test_optional_api_key_valid(self):
        """Test that optional_api_key succeeds with valid API key."""
        valid_key = settings.API_KEY

        with patch("dependencies.logger"):
            result = await optional_api_key(valid_key)
            assert result == valid_key

    @pytest.mark.asyncio
    async def test_optional_api_key_missing(self):
        """Test that optional_api_key returns None with missing API key."""
        with patch("dependencies.logger"):
            result = await optional_api_key(None)
            assert result is None

    @pytest.mark.asyncio
    async def test_optional_api_key_invalid(self):
        """Test that optional_api_key fails with invalid API key."""
        invalid_key = "invalid-key"

        with patch("dependencies.logger"):
            with pytest.raises(AuthHTTPException) as exc_info:
                await optional_api_key(invalid_key)

            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            content = exc_info.value.response_content
            assert content["detail"] == "Invalid API key"
            assert "request_id" in content
            assert "timestamp" in content


class TestDependencies:
    """Legacy test class name for compatibility with test counting."""

    @pytest.mark.asyncio
    async def test_verify_api_key_valid(self):
        """Test dependency with valid API key."""
        valid_key = settings.API_KEY

        with patch("dependencies.logger"):
            result = await verify_api_key(valid_key)
            assert result == valid_key

    @pytest.mark.asyncio
    async def test_verify_api_key_invalid(self):
        """Test dependency with invalid API key."""
        invalid_key = "invalid-key"

        with patch("dependencies.logger"):
            with pytest.raises(AuthHTTPException) as exc_info:
                await verify_api_key(invalid_key)

            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            content = exc_info.value.response_content
            assert content["detail"] == "Invalid API key"

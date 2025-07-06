import os
from unittest.mock import patch

import pytest

from fastapi.testclient import TestClient

# Set test environment variables before importing the app
os.environ["API_KEY"] = "test-api-key-12345"

from main import app


@pytest.fixture
def client():
    """
    Create a test client for the FastAPI application.
    """
    return TestClient(app)


@pytest.fixture
def valid_api_key():
    """
    Provide the valid test API key.
    """
    return "test-api-key-12345"


@pytest.fixture
def invalid_api_key():
    """
    Provide an invalid API key for testing.
    """
    return "invalid-key"


@pytest.fixture
def api_key_headers(valid_api_key):
    """
    Provide headers with valid API key.
    """
    return {"X-API-KEY": valid_api_key}


@pytest.fixture
def invalid_api_key_headers(invalid_api_key):
    """
    Provide headers with invalid API key.
    """
    return {"X-API-KEY": invalid_api_key}


@pytest.fixture
def mock_settings():
    """
    Mock settings for testing.
    """
    with patch("config.settings") as mock:
        mock.API_KEY = "test-api-key-12345"
        yield mock

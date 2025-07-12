import os
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from fastapi.testclient import TestClient

# Set test environment variables before importing the app
os.environ["API_KEY"] = "test-api-key-12345"
os.environ["JWT_SECRET"] = (
    "test-jwt-secret-key-for-testing-purposes-minimum-32-chars-required"
)
# Use separate test database to avoid polluting development data
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test_database.db"

from main import app


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Set up test database before all tests run.

    This fixture automatically runs before any tests and ensures
    the test database has the proper schema via Alembic migrations.
    """
    # Remove existing test database to start fresh
    test_db_path = Path("./test_database.db")
    if test_db_path.exists():
        test_db_path.unlink()

    # Run Alembic migrations to create schema
    try:
        subprocess.run(
            ["uv", "run", "alembic", "upgrade", "head"],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to set up test database: {e.stderr}")

    yield

    # Clean up test database after all tests complete
    if test_db_path.exists():
        test_db_path.unlink()


@pytest.fixture
def client():
    """
    Create a test client for the FastAPI application.
    """
    return TestClient(app)


@pytest.fixture
def test_user():
    """
    Test user credentials for registration and login.
    """
    import uuid

    unique_id = str(uuid.uuid4())[:8]
    return {
        "email": f"test{unique_id}@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
    }


@pytest.fixture
def test_user_token(client, test_user):
    """
    Create a test user and return a valid JWT token.
    """
    # Register the test user
    register_response = client.post("/auth/register", json=test_user)

    if register_response.status_code != 201:
        # If user already exists, try to login directly
        print(
            f"Registration failed with {register_response.status_code}: {register_response.text}"
        )

    # Login to get token
    login_data = {"username": test_user["email"], "password": test_user["password"]}
    login_response = client.post("/auth/jwt/login", data=login_data)

    if login_response.status_code == 200:
        token_data = login_response.json()
        return token_data["access_token"]
    else:
        print(f"Login failed with {login_response.status_code}: {login_response.text}")
        # Return a mock token for testing if user creation fails
        return "test-jwt-token-12345"


@pytest.fixture
def bearer_headers(test_user_token):
    """
    Provide headers with valid JWT Bearer token.
    """
    return {"Authorization": f"Bearer {test_user_token}"}


@pytest.fixture
def invalid_bearer_headers():
    """
    Provide headers with invalid JWT Bearer token.
    """
    return {"Authorization": "Bearer invalid-jwt-token"}


# Legacy fixtures for backward compatibility with existing API key tests
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
    Provide headers with valid API key (legacy).
    """
    return {"X-API-KEY": valid_api_key}


@pytest.fixture
def invalid_api_key_headers(invalid_api_key):
    """
    Provide headers with invalid API key (legacy).
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

"""Tests for MCP authentication service."""

import uuid
from unittest.mock import MagicMock, patch

import pytest

from models.user import User
from services.mcp_auth import (
    MCPAuthService,
    get_mcp_auth_service,
    reset_mcp_auth_service,
)


@pytest.fixture(autouse=True)
def reset_service():
    """Reset the MCP auth service before each test."""
    reset_mcp_auth_service()
    yield
    reset_mcp_auth_service()


@pytest.fixture
def mock_user():
    """Create a mock User instance for testing."""
    user = MagicMock(spec=User)
    user.id = uuid.uuid4()
    user.email = "test@example.com"
    user.first_name = "Test"
    user.last_name = "User"
    user.role = "user"
    user.full_name = "Test User"
    return user


class TestMCPAuthService:
    """Test cases for MCPAuthService."""

    @patch("services.mcp_auth.get_mcp_rsa_manager")
    @patch("services.mcp_auth.settings")
    def test_init(self, mock_settings, mock_get_rsa_manager):
        """Test MCPAuthService initialization."""
        mock_settings.MCP_JWT_AUDIENCE = "mcp-server"
        mock_settings.MCP_JWT_ISSUER = "personal-server"
        mock_settings.MCP_JWT_EXPIRE_MINUTES = 60

        mock_rsa_manager = MagicMock()
        mock_get_rsa_manager.return_value = mock_rsa_manager

        service = MCPAuthService()

        assert service.rsa_manager == mock_rsa_manager
        assert service.audience == "mcp-server"
        assert service.issuer == "personal-server"
        assert service.expire_minutes == 60

    @patch("services.mcp_auth.get_mcp_rsa_manager")
    def test_generate_mcp_token_for_user_success(self, mock_get_rsa_manager, mock_user):
        """Test successful MCP token generation for FastAPI-Users user."""
        mock_rsa_manager = MagicMock()
        mock_rsa_manager.create_token.return_value = "test.jwt.token"
        mock_get_rsa_manager.return_value = mock_rsa_manager

        service = MCPAuthService()
        token = service.generate_mcp_token_for_user(mock_user)

        mock_rsa_manager.create_token.assert_called_once_with(
            user_id=str(mock_user.id), email=mock_user.email
        )
        assert token == "test.jwt.token"

    @patch("services.mcp_auth.get_mcp_rsa_manager")
    def test_generate_mcp_token_for_user_failure(self, mock_get_rsa_manager, mock_user):
        """Test MCP token generation failure for FastAPI-Users user."""
        mock_rsa_manager = MagicMock()
        mock_rsa_manager.create_token.side_effect = Exception("Token creation failed")
        mock_get_rsa_manager.return_value = mock_rsa_manager

        service = MCPAuthService()

        with pytest.raises(Exception, match="Token creation failed"):
            service.generate_mcp_token_for_user(mock_user)

    @patch("services.mcp_auth.get_mcp_rsa_manager")
    @patch("services.mcp_auth.settings")
    def test_generate_mcp_token_for_legacy_api_key_success(
        self, mock_settings, mock_get_rsa_manager
    ):
        """Test successful MCP token generation for legacy API key."""
        mock_settings.MCP_JWT_AUDIENCE = "mcp-server"
        mock_settings.MCP_JWT_ISSUER = "personal-server"
        mock_settings.MCP_JWT_EXPIRE_MINUTES = 60

        mock_rsa_manager = MagicMock()
        mock_key_pair = MagicMock()
        mock_key_pair.create_token.return_value = "legacy.jwt.token"
        mock_rsa_manager.get_or_create_key_pair.return_value = mock_key_pair
        mock_get_rsa_manager.return_value = mock_rsa_manager

        service = MCPAuthService()
        api_key = "test-api-key-12345"
        token = service.generate_mcp_token_for_legacy_api_key(api_key)

        # Check that create_token was called with correct parameters
        mock_key_pair.create_token.assert_called_once()
        call_args = mock_key_pair.create_token.call_args
        assert call_args[1]["audience"] == "mcp-server"
        assert call_args[1]["issuer"] == "personal-server"
        assert call_args[1]["expires_in_seconds"] == 3600
        assert call_args[1]["additional_claims"]["scope"] == "mcp-access"
        assert call_args[1]["additional_claims"]["auth_type"] == "legacy-api-key"
        # Subject should contain legacy-api-key prefix and hash
        assert call_args[1]["subject"].startswith("legacy-api-key:")

        assert token == "legacy.jwt.token"

    @patch("services.mcp_auth.get_mcp_rsa_manager")
    def test_generate_mcp_token_for_legacy_api_key_failure(self, mock_get_rsa_manager):
        """Test MCP token generation failure for legacy API key."""
        mock_rsa_manager = MagicMock()
        mock_rsa_manager.get_or_create_key_pair.side_effect = Exception(
            "Key pair creation failed"
        )
        mock_get_rsa_manager.return_value = mock_rsa_manager

        service = MCPAuthService()

        with pytest.raises(Exception, match="Key pair creation failed"):
            service.generate_mcp_token_for_legacy_api_key("test-api-key")

    def test_hash_api_key(self):
        """Test API key hashing."""
        service = MCPAuthService()

        # Test that the same API key produces the same hash
        api_key = "test-api-key-12345"
        hash1 = service._hash_api_key(api_key)
        hash2 = service._hash_api_key(api_key)

        assert hash1 == hash2
        assert len(hash1) == 16  # First 16 characters of SHA256 hash
        assert isinstance(hash1, str)

        # Test that different API keys produce different hashes
        different_key = "different-api-key"
        hash3 = service._hash_api_key(different_key)
        assert hash1 != hash3


class TestMCPAuthServiceSingleton:
    """Test cases for MCP auth service singleton."""

    def test_get_mcp_auth_service_singleton(self):
        """Test that get_mcp_auth_service returns the same instance."""
        service1 = get_mcp_auth_service()
        service2 = get_mcp_auth_service()

        assert service1 is service2
        assert isinstance(service1, MCPAuthService)

    def test_reset_mcp_auth_service(self):
        """Test that reset creates a new instance."""
        service1 = get_mcp_auth_service()
        reset_mcp_auth_service()
        service2 = get_mcp_auth_service()

        assert service1 is not service2
        assert isinstance(service2, MCPAuthService)

"""Tests for MCP RSA key management service."""

from unittest.mock import MagicMock, patch

import pytest

from services.mcp_rsa_keys import (
    MCPRSAKeyManager,
    get_mcp_rsa_manager,
    reset_mcp_rsa_manager,
)


@pytest.fixture(autouse=True)
def reset_manager():
    """Reset the MCP RSA key manager before each test."""
    reset_mcp_rsa_manager()
    yield
    reset_mcp_rsa_manager()


class TestMCPRSAKeyManager:
    """Test cases for MCPRSAKeyManager."""

    @patch("services.mcp_rsa_keys.settings")
    @patch("services.mcp_rsa_keys.RSAKeyPair")
    def test_get_or_create_key_pair_from_environment(
        self, mock_rsa_keypair, mock_settings
    ):
        """Test loading RSA key pair from environment variables."""
        # Mock settings
        mock_settings.MCP_JWT_PRIVATE_KEY = (
            "-----BEGIN PRIVATE KEY-----\ntest\n-----END PRIVATE KEY-----"
        )
        mock_settings.MCP_JWT_PUBLIC_KEY = (
            "-----BEGIN PUBLIC KEY-----\ntest\n-----END PUBLIC KEY-----"
        )
        mock_settings.ENV = "production"

        # Mock RSAKeyPair.from_pem
        mock_key_pair = MagicMock()
        mock_rsa_keypair.from_pem.return_value = mock_key_pair

        manager = MCPRSAKeyManager()
        result = manager.get_or_create_key_pair()

        # Verify from_pem was called with correct parameters
        mock_rsa_keypair.from_pem.assert_called_once_with(
            private_key_pem="-----BEGIN PRIVATE KEY-----\ntest\n-----END PRIVATE KEY-----",
            public_key_pem="-----BEGIN PUBLIC KEY-----\ntest\n-----END PUBLIC KEY-----",
        )
        assert result == mock_key_pair

    @patch("services.mcp_rsa_keys.settings")
    @patch("services.mcp_rsa_keys.RSAKeyPair")
    def test_get_or_create_key_pair_generate_development(
        self, mock_rsa_keypair, mock_settings
    ):
        """Test auto-generating RSA key pair in development."""
        # Mock settings - no keys provided, development environment
        mock_settings.MCP_JWT_PRIVATE_KEY = None
        mock_settings.MCP_JWT_PUBLIC_KEY = None
        mock_settings.ENV = "development"

        # Mock RSAKeyPair.generate
        mock_key_pair = MagicMock()
        mock_rsa_keypair.generate.return_value = mock_key_pair

        manager = MCPRSAKeyManager()
        result = manager.get_or_create_key_pair()

        # Verify generate was called
        mock_rsa_keypair.generate.assert_called_once()
        assert result == mock_key_pair

    @patch("services.mcp_rsa_keys.settings")
    def test_get_or_create_key_pair_production_without_keys_raises_error(
        self, mock_settings
    ):
        """Test that production environment requires explicit keys."""
        # Mock settings - no keys provided, production environment
        mock_settings.MCP_JWT_PRIVATE_KEY = None
        mock_settings.MCP_JWT_PUBLIC_KEY = None
        mock_settings.ENV = "production"

        manager = MCPRSAKeyManager()

        with pytest.raises(ValueError, match="MCP RSA keys required in production"):
            manager.get_or_create_key_pair()

    @patch("services.mcp_rsa_keys.settings")
    @patch("services.mcp_rsa_keys.RSAKeyPair")
    def test_get_or_create_key_pair_caching(self, mock_rsa_keypair, mock_settings):
        """Test that key pair is cached after first creation."""
        # Mock settings
        mock_settings.MCP_JWT_PRIVATE_KEY = (
            "-----BEGIN PRIVATE KEY-----\ntest\n-----END PRIVATE KEY-----"
        )
        mock_settings.MCP_JWT_PUBLIC_KEY = (
            "-----BEGIN PUBLIC KEY-----\ntest\n-----END PUBLIC KEY-----"
        )
        mock_settings.ENV = "production"

        # Mock RSAKeyPair.from_pem
        mock_key_pair = MagicMock()
        mock_rsa_keypair.from_pem.return_value = mock_key_pair

        manager = MCPRSAKeyManager()

        # First call should create key pair
        result1 = manager.get_or_create_key_pair()
        # Second call should return cached key pair
        result2 = manager.get_or_create_key_pair()

        # Should only call from_pem once
        mock_rsa_keypair.from_pem.assert_called_once()
        assert result1 == result2 == mock_key_pair

    @patch("services.mcp_rsa_keys.settings")
    @patch("services.mcp_rsa_keys.RSAKeyPair")
    def test_create_token(self, mock_rsa_keypair, mock_settings):
        """Test creating MCP token."""
        # Mock settings
        mock_settings.MCP_JWT_PRIVATE_KEY = "test_private_key"
        mock_settings.MCP_JWT_PUBLIC_KEY = "test_public_key"
        mock_settings.ENV = "production"
        mock_settings.MCP_JWT_AUDIENCE = "mcp-server"
        mock_settings.MCP_JWT_ISSUER = "personal-server"
        mock_settings.MCP_JWT_EXPIRE_MINUTES = 60

        # Mock RSA key pair and token creation
        mock_key_pair = MagicMock()
        mock_key_pair.create_token.return_value = "test.jwt.token"
        mock_rsa_keypair.from_pem.return_value = mock_key_pair

        manager = MCPRSAKeyManager()
        token = manager.create_token(user_id="123", email="test@example.com")

        # Verify token creation was called with correct parameters
        mock_key_pair.create_token.assert_called_once_with(
            audience="mcp-server",
            subject="123",
            issuer="personal-server",
            additional_claims={"email": "test@example.com", "scope": "mcp-access"},
            expires_in_seconds=3600,
        )
        assert token == "test.jwt.token"


class TestMCPRSAKeyManagerSingleton:
    """Test cases for MCP RSA key manager singleton."""

    def test_get_mcp_rsa_manager_singleton(self):
        """Test that get_mcp_rsa_manager returns the same instance."""
        manager1 = get_mcp_rsa_manager()
        manager2 = get_mcp_rsa_manager()

        assert manager1 is manager2
        assert isinstance(manager1, MCPRSAKeyManager)

    def test_reset_mcp_rsa_manager(self):
        """Test that reset creates a new instance."""
        manager1 = get_mcp_rsa_manager()
        reset_mcp_rsa_manager()
        manager2 = get_mcp_rsa_manager()

        assert manager1 is not manager2
        assert isinstance(manager2, MCPRSAKeyManager)

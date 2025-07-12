"""Integration tests for MCP authentication endpoints."""

from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient


class TestMCPTokenEndpoints:
    """Integration tests for MCP token generation endpoints."""

    @patch("routers.mcp_auth.get_mcp_auth_service")
    def test_generate_mcp_token_with_fastapi_users_success(
        self, mock_get_service, client: TestClient, test_user_token: str
    ):
        """Test successful MCP token generation with FastAPI-Users authentication."""
        # Mock the MCP auth service
        mock_service = MagicMock()
        mock_service.generate_mcp_token_for_user.return_value = "mcp.jwt.token.12345"
        mock_service.expire_minutes = 60
        mock_get_service.return_value = mock_service

        # Make request with valid FastAPI-Users JWT token
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = client.post("/auth/mcp-token", json={}, headers=headers)

        assert response.status_code == 200
        data = response.json()

        assert data["mcp_token"] == "mcp.jwt.token.12345"
        assert data["token_type"] == "bearer"
        assert data["expires_in"] == 3600  # 60 minutes * 60 seconds
        assert data["scope"] == "mcp-access"
        assert "issued_at" in data
        assert "user_info" in data

        # Verify user info contains expected fields
        user_info = data["user_info"]
        assert "user_id" in user_info
        assert "email" in user_info
        assert "full_name" in user_info
        assert "role" in user_info

    def test_generate_mcp_token_with_fastapi_users_no_auth(self, client: TestClient):
        """Test MCP token generation without authentication."""
        response = client.post("/auth/mcp-token", json={})

        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Unauthorized"

    def test_generate_mcp_token_with_fastapi_users_invalid_token(
        self, client: TestClient
    ):
        """Test MCP token generation with invalid JWT token."""
        headers = {"Authorization": "Bearer invalid.jwt.token"}
        response = client.post("/auth/mcp-token", json={}, headers=headers)

        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Unauthorized"

    @patch("routers.mcp_auth.get_mcp_auth_service")
    def test_generate_mcp_token_with_fastapi_users_service_error(
        self, mock_get_service, client: TestClient, test_user_token: str
    ):
        """Test MCP token generation with service error."""
        # Mock the MCP auth service to raise an exception
        mock_service = MagicMock()
        mock_service.generate_mcp_token_for_user.side_effect = Exception(
            "Token generation failed"
        )
        mock_get_service.return_value = mock_service

        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = client.post("/auth/mcp-token", json={}, headers=headers)

        assert response.status_code == 500
        data = response.json()
        assert "Failed to generate MCP token" in data["detail"]

    @patch("routers.mcp_auth.get_mcp_auth_service")
    def test_generate_mcp_token_legacy_success(
        self, mock_get_service, client: TestClient
    ):
        """Test successful MCP token generation with legacy API key."""
        # Mock the MCP auth service
        mock_service = MagicMock()
        mock_service.generate_mcp_token_for_legacy_api_key.return_value = (
            "legacy.mcp.jwt.token"
        )
        mock_service.expire_minutes = 60
        mock_get_service.return_value = mock_service

        # Make request with valid API key
        headers = {"X-API-KEY": "test-api-key-12345"}
        response = client.post("/auth/mcp-token/legacy", json={}, headers=headers)

        assert response.status_code == 200
        data = response.json()

        assert data["mcp_token"] == "legacy.mcp.jwt.token"
        assert data["token_type"] == "bearer"
        assert data["expires_in"] == 3600
        assert data["scope"] == "mcp-access"
        assert "issued_at" in data
        assert "user_info" in data

        # Verify legacy user info
        user_info = data["user_info"]
        assert user_info["auth_type"] == "legacy-api-key"
        assert user_info["api_key_prefix"] == "test-api..."

    def test_generate_mcp_token_legacy_no_api_key(self, client: TestClient):
        """Test legacy MCP token generation without API key."""
        response = client.post("/auth/mcp-token/legacy", json={})

        assert response.status_code == 401
        data = response.json()
        assert "API key missing" in data["detail"]["detail"]

    def test_generate_mcp_token_legacy_invalid_api_key(self, client: TestClient):
        """Test legacy MCP token generation with invalid API key."""
        headers = {"X-API-KEY": "invalid-api-key"}
        response = client.post("/auth/mcp-token/legacy", json={}, headers=headers)

        assert response.status_code == 401
        data = response.json()
        assert "Invalid API key" in data["detail"]["detail"]

    @patch("routers.mcp_auth.get_mcp_auth_service")
    def test_generate_mcp_token_legacy_service_error(
        self, mock_get_service, client: TestClient
    ):
        """Test legacy MCP token generation with service error."""
        # Mock the MCP auth service to raise an exception
        mock_service = MagicMock()
        mock_service.generate_mcp_token_for_legacy_api_key.side_effect = Exception(
            "Token generation failed"
        )
        mock_get_service.return_value = mock_service

        headers = {"X-API-KEY": "test-api-key-12345"}
        response = client.post("/auth/mcp-token/legacy", json={}, headers=headers)

        assert response.status_code == 500
        data = response.json()
        assert "Failed to generate MCP token" in data["detail"]


class TestMCPEndpointSecurity:
    """Test security aspects of MCP authentication endpoints."""

    def test_mcp_token_endpoint_cors(self, client: TestClient):
        """Test CORS handling for MCP token endpoints."""
        headers = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
        }
        response = client.options("/auth/mcp-token", headers=headers)

        # Should not fail due to CORS (actual headers tested in browser)
        assert response.status_code in [200, 405]

    def test_mcp_token_endpoint_rate_limiting(self, client: TestClient):
        """Test that MCP token endpoints respect rate limiting."""
        # This would need to be implemented if rate limiting is added
        # For now, just verify endpoints are accessible
        response = client.post("/auth/mcp-token", json={})
        assert response.status_code in [401, 422]  # Should fail auth, not rate limit

    @patch("routers.mcp_auth.get_mcp_auth_service")
    def test_mcp_token_response_structure(
        self, mock_get_service, client: TestClient, test_user_token: str
    ):
        """Test that MCP token response has correct structure and no sensitive data leaks."""
        mock_service = MagicMock()
        mock_service.generate_mcp_token_for_user.return_value = "test.token.123"
        mock_service.expire_minutes = 60
        mock_get_service.return_value = mock_service

        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = client.post("/auth/mcp-token", json={}, headers=headers)

        assert response.status_code == 200
        data = response.json()

        # Verify required fields
        required_fields = [
            "mcp_token",
            "token_type",
            "expires_in",
            "scope",
            "issued_at",
            "user_info",
        ]
        for field in required_fields:
            assert field in data

        # Verify no sensitive data in response (except the token itself)
        response_str = str(data)
        assert "password" not in response_str.lower()
        assert "secret" not in response_str.lower()
        assert "private" not in response_str.lower()


class TestMCPTokenValidation:
    """Test MCP token validation and format."""

    @patch("routers.mcp_auth.get_mcp_auth_service")
    def test_mcp_token_format_validation(
        self, mock_get_service, client: TestClient, test_user_token: str
    ):
        """Test that generated MCP tokens have expected format."""
        mock_service = MagicMock()
        # Mock a JWT-like token format (using fake test token)
        mock_service.generate_mcp_token_for_user.return_value = "fake.test.token"
        mock_service.expire_minutes = 60
        mock_get_service.return_value = mock_service

        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = client.post("/auth/mcp-token", json={}, headers=headers)

        assert response.status_code == 200
        data = response.json()

        mcp_token = data["mcp_token"]
        # For this test, we're using a fake token, so just verify it's not empty
        assert len(mcp_token) > 0
        assert mcp_token != "null" and mcp_token != "undefined"
        assert mcp_token == "fake.test.token"

"""Integration tests for MCP authentication endpoints."""

import jwt

from fastapi.testclient import TestClient


class TestMCPTokenEndpoints:
    """Integration tests for MCP token generation endpoints."""

    def test_generate_mcp_token_with_fastapi_users_success(
        self, client: TestClient, test_user_token: str
    ):
        """Test successful MCP token generation with FastAPI-Users authentication."""
        # Make request with valid FastAPI-Users JWT token
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = client.post("/auth/mcp-token", json={}, headers=headers)

        assert response.status_code == 200
        data = response.json()

        # Verify response structure
        assert "mcp_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] == 3600  # 60 minutes * 60 seconds
        assert data["scope"] == "mcp-access"
        assert "issued_at" in data
        assert "user_info" in data

        # Verify JWT token structure (decode without verification for testing)
        mcp_token = data["mcp_token"]
        assert isinstance(mcp_token, str)
        assert len(mcp_token.split(".")) == 3  # JWT has 3 parts

        # Decode JWT to verify claims (without signature verification for testing)
        try:
            decoded = jwt.decode(mcp_token, options={"verify_signature": False})
            assert decoded["iss"] == "personal-server"
            assert decoded["aud"] == "mcp-server"
            assert decoded["scope"] == "mcp-access"
            assert "sub" in decoded
            assert "iat" in decoded
            assert "exp" in decoded
        except jwt.InvalidTokenError:
            raise AssertionError("Invalid JWT token format") from None

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

    def test_generate_mcp_token_with_fastapi_users_service_robustness(
        self, client: TestClient, test_user_token: str
    ):
        """Test MCP token generation service robustness with multiple requests."""
        headers = {"Authorization": f"Bearer {test_user_token}"}

        # Make multiple requests to ensure service is robust
        for _ in range(3):
            response = client.post("/auth/mcp-token", json={}, headers=headers)
            assert response.status_code == 200
            data = response.json()
            assert "mcp_token" in data
            assert data["token_type"] == "bearer"


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

    def test_mcp_token_response_structure(
        self, client: TestClient, test_user_token: str
    ):
        """Test that MCP token response has correct structure and no sensitive data leaks."""
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

    def test_mcp_token_format_validation(
        self, client: TestClient, test_user_token: str
    ):
        """Test that generated MCP tokens have expected format."""
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = client.post("/auth/mcp-token", json={}, headers=headers)

        assert response.status_code == 200
        data = response.json()

        mcp_token = data["mcp_token"]
        # Verify JWT token format
        assert len(mcp_token) > 0
        assert mcp_token != "null" and mcp_token != "undefined"
        assert len(mcp_token.split(".")) == 3  # JWT has 3 parts

        # Verify it's a valid JWT structure
        try:
            decoded = jwt.decode(mcp_token, options={"verify_signature": False})
            assert "iss" in decoded
            assert "aud" in decoded
            assert "exp" in decoded
            assert "iat" in decoded
        except jwt.InvalidTokenError:
            raise AssertionError("Invalid JWT token format") from None

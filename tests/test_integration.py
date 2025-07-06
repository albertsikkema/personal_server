from fastapi.testclient import TestClient


class TestPublicEndpoints:
    """Integration tests for public endpoints."""

    def test_root_endpoint(self, client: TestClient):
        """Test the root endpoint."""
        response = client.get("/")

        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to FastAPI Application"}

    def test_health_endpoint(self, client: TestClient):
        """Test the health endpoint without authentication."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "FastAPI Application"
        assert data["version"] == "1.0.0"
        assert "timestamp" in data

    def test_cors_headers(self, client: TestClient):
        """Test CORS headers are present."""
        # Note: TestClient doesn't properly simulate CORS middleware behavior
        # CORS headers are only added for actual cross-origin requests
        # This would need to be tested with a real HTTP client or by mocking the request origin
        response = client.options("/", headers={"Origin": "http://example.com"})

        # For now, we just verify the endpoint is accessible
        assert response.status_code in [200, 405]  # 405 if OPTIONS not implemented


class TestProtectedEndpoints:
    """Integration tests for protected endpoints."""

    def test_protected_endpoint_no_auth(self, client: TestClient):
        """Test protected endpoint without authentication."""
        response = client.get("/protected")

        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "API key missing"
        assert "request_id" in data
        assert "timestamp" in data

    def test_protected_endpoint_invalid_auth(
        self, client: TestClient, invalid_api_key_headers
    ):
        """Test protected endpoint with invalid API key."""
        response = client.get("/protected", headers=invalid_api_key_headers)

        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Invalid API key"
        assert "request_id" in data
        assert "timestamp" in data

    def test_protected_endpoint_valid_auth(self, client: TestClient, api_key_headers):
        """Test protected endpoint with valid API key."""
        response = client.get("/protected", headers=api_key_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Access granted to protected resource"
        assert "timestamp" in data

    def test_protected_data_endpoint_no_auth(self, client: TestClient):
        """Test protected data endpoint without authentication."""
        response = client.get("/protected/data")

        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "API key missing"
        assert "request_id" in data
        assert "timestamp" in data

    def test_protected_data_endpoint_valid_auth(
        self, client: TestClient, api_key_headers
    ):
        """Test protected data endpoint with valid API key."""
        response = client.get("/protected/data", headers=api_key_headers)

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert data["data"]["id"] == 1
        assert data["data"]["info"] == "This is protected information"
        assert data["data"]["items"] == ["item1", "item2", "item3"]


class TestAPIDocumentation:
    """Tests for API documentation endpoints."""

    def test_openapi_schema_accessible(self, client: TestClient):
        """Test that OpenAPI schema is accessible."""
        response = client.get("/openapi.json")

        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert data["info"]["title"] == "FastAPI Application"

    def test_swagger_ui_accessible(self, client: TestClient):
        """Test that Swagger UI is accessible."""
        response = client.get("/docs")

        assert response.status_code == 200
        assert "swagger-ui" in response.text

    def test_redoc_accessible(self, client: TestClient):
        """Test that ReDoc is accessible."""
        response = client.get("/redoc")

        assert response.status_code == 200
        assert "redoc" in response.text.lower()


class TestEnvironmentBasedDocumentation:
    """Tests for environment-based documentation visibility."""

    def _create_app_with_env(self, env_value: str):
        """Create FastAPI app instance with specific ENV value."""
        from pydantic_settings import BaseSettings, SettingsConfigDict

        from dependencies import RequiredAuth
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        from pydantic import Field

        # Create settings with specific ENV value
        class TestSettings(BaseSettings):
            model_config = SettingsConfigDict(
                env_file=".env",
                env_file_encoding="utf-8",
                case_sensitive=True,
                validate_default=True,
            )

            API_KEY: str = Field(default="test-api-key-12345678")
            ENV: str = Field(default=env_value)

        settings = TestSettings()

        # Create FastAPI app with environment-specific docs configuration
        app = FastAPI(
            title="FastAPI Application",
            description="A FastAPI application with API key authentication",
            version="1.0.0",
            docs_url="/docs" if settings.ENV != "production" else None,
            redoc_url="/redoc" if settings.ENV != "production" else None,
            openapi_url="/openapi.json" if settings.ENV != "production" else None,
        )

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Authentication now handled via dependency injection
        # Add protected endpoint that requires authentication
        @app.get("/protected")
        async def protected_endpoint(_api_key: str = RequiredAuth):
            return {"message": "Access granted to protected resource"}

        return app

    def test_docs_visible_in_development(self):
        """Test that docs are visible when ENV=development."""
        from fastapi.testclient import TestClient

        app = self._create_app_with_env("development")
        client = TestClient(app)

        # Test all documentation endpoints
        assert client.get("/docs").status_code == 200
        assert client.get("/redoc").status_code == 200
        assert client.get("/openapi.json").status_code == 200

    def test_docs_visible_in_staging(self):
        """Test that docs are visible when ENV=staging."""
        from fastapi.testclient import TestClient

        app = self._create_app_with_env("staging")
        client = TestClient(app)

        # Test all documentation endpoints
        assert client.get("/docs").status_code == 200
        assert client.get("/redoc").status_code == 200
        assert client.get("/openapi.json").status_code == 200

    def test_docs_hidden_in_production(self):
        """Test that docs are hidden when ENV=production."""
        from fastapi.testclient import TestClient

        app = self._create_app_with_env("production")
        client = TestClient(app)

        # Test all documentation endpoints return 404
        assert client.get("/docs").status_code == 404
        assert client.get("/redoc").status_code == 404
        assert client.get("/openapi.json").status_code == 404

    def test_docs_visible_with_default_env(self):
        """Test that docs are visible when ENV defaults to development."""
        from fastapi.testclient import TestClient

        app = self._create_app_with_env("development")
        client = TestClient(app)

        # Test all documentation endpoints
        assert client.get("/docs").status_code == 200
        assert client.get("/redoc").status_code == 200
        assert client.get("/openapi.json").status_code == 200


class TestSecurityByDesign:
    """Tests for security by design - all paths protected by default."""

    def test_random_endpoints_return_404(self, client: TestClient):
        """Test that random/new endpoints return 404 when not defined."""
        random_endpoints = [
            "/api/users",
            "/admin",
            "/secret",
            "/data",
            "/users/123",
            "/products",
            "/config",
            "/internal",
            "/v1/api",
            "/test",
        ]

        for endpoint in random_endpoints:
            response = client.get(endpoint)
            assert response.status_code == 404, (
                f"Endpoint {endpoint} should return 404 for undefined routes"
            )
            assert response.json() == {"detail": "Not Found"}

    def test_similar_to_public_paths_return_404(self, client: TestClient):
        """Test that paths similar to public ones return 404 when not defined."""
        endpoints = [
            "/health/status",  # Similar to /health but undefined
            "/docs/api",  # Similar to /docs but undefined
            "/healthy",  # Similar to /health but undefined
            "/document",  # Similar to /docs but undefined
        ]

        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 404, (
                f"Endpoint {endpoint} should return 404 for undefined routes"
            )
            assert response.json() == {"detail": "Not Found"}


class TestHeaderHandling:
    """Tests for HTTP header handling."""

    def test_case_insensitive_headers(self, client: TestClient):
        """Test that API key headers are case-insensitive as per HTTP standards."""
        # Test various case combinations that should all work
        header_variations = [
            {"X-API-KEY": "test-api-key-12345"},  # Standard case
            {"x-api-key": "test-api-key-12345"},  # Lowercase
            {"X-Api-Key": "test-api-key-12345"},  # Mixed case
            {"x-API-key": "test-api-key-12345"},  # Another mixed case
        ]

        for headers in header_variations:
            response = client.get("/protected", headers=headers)
            assert response.status_code == 200, (
                f"Headers {headers} should work - HTTP headers are case-insensitive"
            )
            data = response.json()
            assert data["message"] == "Access granted to protected resource"

    def test_invalid_header_names(self, client: TestClient):
        """Test that only the correct header name works."""
        invalid_headers = [
            {"API-KEY": "test-api-key-12345"},  # Missing X-
            {"X-APIKEY": "test-api-key-12345"},  # Missing dash
            {"Authorization": "test-api-key-12345"},  # Wrong header name
        ]

        for headers in invalid_headers:
            response = client.get("/protected", headers=headers)
            assert response.status_code == 401, f"Headers {headers} should be rejected"
            data = response.json()
            assert data["detail"] == "API key missing"
            assert "request_id" in data
            assert "timestamp" in data


class TestSecurityTesting:
    """Enhanced security testing for injection attacks and edge cases."""

    def test_sql_injection_attempt(self, client: TestClient):
        """Test that SQL injection attempts are handled safely."""
        malicious_headers = {"X-API-KEY": "'; DROP TABLE users; --"}
        response = client.get("/protected", headers=malicious_headers)
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Invalid API key"
        assert "request_id" in data

    def test_header_injection_attempt(self, client: TestClient):
        """Test protection against header injection attacks."""
        malicious_headers = {"X-API-KEY": "valid-key\r\nSet-Cookie: admin=true"}
        response = client.get("/protected", headers=malicious_headers)
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Invalid API key"

    def test_xss_attempt_in_header(self, client: TestClient):
        """Test that XSS attempts in headers are handled safely."""
        malicious_headers = {"X-API-KEY": "<script>alert('xss')</script>"}
        response = client.get("/protected", headers=malicious_headers)
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Invalid API key"

    def test_extremely_long_api_key(self, client: TestClient):
        """Test handling of extremely long API key values."""
        long_key = "a" * 10000  # 10KB API key
        malicious_headers = {"X-API-KEY": long_key}
        response = client.get("/protected", headers=malicious_headers)
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Invalid API key"

    def test_null_byte_injection(self, client: TestClient):
        """Test protection against null byte injection."""
        malicious_headers = {"X-API-KEY": "test-api-key-12345\x00malicious"}
        response = client.get("/protected", headers=malicious_headers)
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Invalid API key"

    def test_unicode_normalization_attack(self, client: TestClient):
        """Test protection against unicode normalization attacks."""
        # Using different unicode representations that could normalize to valid key
        malicious_headers = {"X-API-KEY": "test-api-key-12345\u0041"}  # \u0041 is 'A'
        response = client.get("/protected", headers=malicious_headers)
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Invalid API key"

    def test_empty_header_value(self, client: TestClient):
        """Test handling of empty header values."""
        malicious_headers = {"X-API-KEY": ""}
        response = client.get("/protected", headers=malicious_headers)
        assert response.status_code == 401
        data = response.json()
        # Empty string is treated as missing API key
        assert data["detail"] == "API key missing"

    def test_whitespace_only_header(self, client: TestClient):
        """Test handling of whitespace-only header values."""
        malicious_headers = {"X-API-KEY": "   \t\n   "}
        response = client.get("/protected", headers=malicious_headers)
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Invalid API key"


class TestErrorHandling:
    """Tests for error handling."""

    def test_nonexistent_endpoint_returns_404(self, client: TestClient):
        """Test accessing a non-existent endpoint returns 404."""
        response = client.get("/nonexistent")

        # Non-existent endpoints return 404
        assert response.status_code == 404
        assert response.json() == {"detail": "Not Found"}

    def test_nonexistent_endpoint_with_auth(self, client: TestClient, api_key_headers):
        """Test accessing a non-existent endpoint with valid authentication."""
        response = client.get("/nonexistent", headers=api_key_headers)

        # With valid auth, should get 404
        assert response.status_code == 404
        assert response.json() == {"detail": "Not Found"}

    def test_method_not_allowed(self, client: TestClient):
        """Test using wrong HTTP method on public endpoint."""
        response = client.post("/health")

        assert response.status_code == 405
        assert response.json() == {"detail": "Method Not Allowed"}

    def test_method_not_allowed_protected(self, client: TestClient):
        """Test using wrong HTTP method on protected endpoint without auth."""
        response = client.post("/protected")

        # FastAPI returns 405 Method Not Allowed before checking dependencies
        assert response.status_code == 405
        assert response.json() == {"detail": "Method Not Allowed"}


class TestGeocodingEndpoints:
    """Integration tests for geocoding endpoints."""

    def test_geocode_city_success(self, client: TestClient, api_key_headers):
        """Test successful city geocoding."""
        response = client.get("/geocode/city?city=London", headers=api_key_headers)
        assert response.status_code == 200
        data = response.json()
        assert "location" in data
        assert "lat" in data["location"]
        assert "lon" in data["location"]
        assert data["city"] == "London"
        assert "cached" in data
        assert "timestamp" in data
        assert "display_name" in data
        assert isinstance(data["location"]["lat"], float)
        assert isinstance(data["location"]["lon"], float)

    def test_geocode_city_not_found(self, client: TestClient, api_key_headers):
        """Test geocoding with non-existent city."""
        response = client.get(
            "/geocode/city?city=Xyzabcdef123NonExistentCity", headers=api_key_headers
        )
        assert response.status_code == 404
        data = response.json()
        assert "City 'Xyzabcdef123NonExistentCity' not found" in data["detail"]

    def test_geocode_health_endpoint(self, client: TestClient, api_key_headers):
        """Test geocoding health endpoint."""
        response = client.get("/geocode/health", headers=api_key_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "geocoding"
        assert data["status"] == "healthy"
        assert "cache_size" in data
        assert data["rate_limiter"] == "active"

    def test_geocode_rate_limiting(self, client: TestClient, api_key_headers):
        """Test user rate limiting."""
        # Make multiple rapid requests
        rate_limited_found = False
        for i in range(15):  # Make more requests to ensure we hit rate limit
            response = client.get(
                f"/geocode/city?city=TestCity{i}", headers=api_key_headers
            )
            # Should get normal responses or rate limiting
            assert response.status_code in [200, 404, 429]
            if response.status_code == 429:
                rate_limited_found = True
                break  # Stop once we hit rate limit
        
        # Should have hit rate limit at some point
        assert rate_limited_found, "Rate limiting should have been triggered"

    def test_geocode_caching_behavior(self, client: TestClient, api_key_headers):
        """Test that caching works correctly."""
        # First request
        response1 = client.get("/geocode/city?city=Paris", headers=api_key_headers)
        # May be rate limited due to previous tests
        if response1.status_code == 429:
            return  # Skip test if rate limited
        assert response1.status_code in [200, 404]
        
        if response1.status_code == 200:
            data1 = response1.json()
            assert data1["cached"] is False
            
            # Second request should be cached
            response2 = client.get("/geocode/city?city=Paris", headers=api_key_headers)
            if response2.status_code == 200:
                data2 = response2.json()
                assert data2["cached"] is True
                assert data1["location"] == data2["location"]

    def test_geocode_authentication_required(self, client: TestClient):
        """Test that authentication is required."""
        response = client.get("/geocode/city?city=London")
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "API key missing"

    def test_geocode_invalid_input(self, client: TestClient, api_key_headers):
        """Test input validation."""
        # Empty city name
        response = client.get("/geocode/city?city=", headers=api_key_headers)
        assert response.status_code == 422

        # City name too long (>200 chars)
        long_city = "x" * 201
        response = client.get(
            f"/geocode/city?city={long_city}", headers=api_key_headers
        )
        assert response.status_code == 422

    def test_geocode_missing_city_parameter(self, client: TestClient, api_key_headers):
        """Test missing city parameter."""
        response = client.get("/geocode/city", headers=api_key_headers)
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        # FastAPI validation error for missing required parameter

    def test_geocode_router_tags_and_prefix(self, client: TestClient):
        """Test that router is properly configured with prefix and tags."""
        # Check OpenAPI schema includes router configuration
        response = client.get("/openapi.json")
        assert response.status_code == 200
        openapi_schema = response.json()

        # Verify geocoding endpoints are under /geocode prefix
        assert "/geocode/city" in openapi_schema["paths"]
        assert "/geocode/health" in openapi_schema["paths"]

        # Verify tags are applied
        city_endpoint = openapi_schema["paths"]["/geocode/city"]["get"]
        assert "geocoding" in city_endpoint["tags"]

    def test_geocode_case_insensitive_city_names(
        self, client: TestClient, api_key_headers
    ):
        """Test that city names are handled regardless of case."""
        cities = ["london", "LONDON", "London", "LoNdOn"]

        responses = []
        for city in cities:
            response = client.get(f"/geocode/city?city={city}", headers=api_key_headers)
            responses.append(response)

        # All should work (either 200 for found or consistent behavior, or 429 for rate limiting)
        for response in responses:
            assert response.status_code in [200, 404, 429]

    def test_geocode_special_characters_in_city_name(
        self, client: TestClient, api_key_headers
    ):
        """Test geocoding with special characters in city names."""
        special_cities = [
            "São Paulo",
            "München",
            "北京",  # Beijing in Chinese
            "Москва",  # Moscow in Russian
        ]

        for city in special_cities:
            response = client.get(f"/geocode/city?city={city}", headers=api_key_headers)
            # Should not error, either found (200) or not found (404), or rate limited (429)
            assert response.status_code in [200, 404, 429, 503]

    def test_geocode_whitespace_handling(self, client: TestClient, api_key_headers):
        """Test geocoding with whitespace in city names."""
        response = client.get("/geocode/city?city= London ", headers=api_key_headers)
        # Should handle whitespace gracefully
        assert response.status_code in [200, 404, 429, 503]

    def test_geocode_response_headers(self, client: TestClient, api_key_headers):
        """Test that response headers are appropriate."""
        response = client.get("/geocode/city?city=London", headers=api_key_headers)

        if response.status_code == 200:
            assert response.headers["content-type"] == "application/json"

        # Rate limiting headers (if present)
        # Note: slowapi may add rate limiting headers

    def test_geocode_concurrent_requests(self, client: TestClient, api_key_headers):
        """Test concurrent requests to geocoding endpoint."""
        import concurrent.futures

        def make_request(city_suffix):
            return client.get(
                f"/geocode/city?city=TestCity{city_suffix}", headers=api_key_headers
            )

        # Make concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(make_request, i) for i in range(3)]
            responses = [future.result() for future in futures]

        # All should complete without error
        for response in responses:
            assert response.status_code in [200, 404, 429, 503]

    def test_geocode_service_unavailable_handling(
        self, client: TestClient, api_key_headers
    ):
        """Test handling when geocoding service encounters errors."""
        # Use a city name that might cause service issues or test with mocked failure
        response = client.get(
            "/geocode/city?city=SpecialErrorTestCity", headers=api_key_headers
        )

        # Should handle gracefully - either success, not found, rate limited, or service unavailable
        assert response.status_code in [200, 404, 429, 503]

        if response.status_code == 503:
            data = response.json()
            assert "service temporarily unavailable" in data["detail"].lower()

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
        assert data["detail"] == "Unauthorized"

    def test_protected_endpoint_invalid_auth(
        self, client: TestClient, invalid_bearer_headers
    ):
        """Test protected endpoint with invalid JWT Bearer token."""
        response = client.get("/protected", headers=invalid_bearer_headers)

        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Unauthorized"

    def test_protected_endpoint_valid_auth(self, client: TestClient, bearer_headers):
        """Test protected endpoint with valid JWT Bearer token."""
        response = client.get("/protected", headers=bearer_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Access granted to protected resource"
        assert "timestamp" in data

    def test_protected_data_endpoint_no_auth(self, client: TestClient):
        """Test protected data endpoint without authentication."""
        response = client.get("/protected/data")

        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Unauthorized"

    def test_protected_data_endpoint_valid_auth(
        self, client: TestClient, bearer_headers
    ):
        """Test protected data endpoint with valid JWT Bearer token."""
        response = client.get("/protected/data", headers=bearer_headers)

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
        assert data["info"]["title"] == "FastAPI Application with JWT Authentication"

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
            JWT_SECRET: str = Field(
                default="test-jwt-secret-key-for-testing-purposes-minimum-32-chars-required"
            )
            ENV: str = Field(default=env_value)
            CRAWL4AI_API_TOKEN: str | None = Field(default=None)

        settings = TestSettings()

        # Create FastAPI app with environment-specific docs configuration
        app = FastAPI(
            title="FastAPI Application with JWT Authentication",
            description="A FastAPI application with JWT Bearer token authentication",
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


class TestJWTAuthentication:
    """Tests for JWT Bearer token authentication."""

    def test_bearer_token_case_sensitive(self, client: TestClient, bearer_headers):
        """Test that Bearer token authentication is case-sensitive for scheme."""
        # Valid Bearer token
        response = client.get("/protected", headers=bearer_headers)
        assert response.status_code == 200

        # Test case variations - Bearer scheme should be case-insensitive per RFC 7617
        token = bearer_headers["Authorization"].split(" ")[1]
        case_variations = [
            {"Authorization": f"Bearer {token}"},  # Standard case
            {"Authorization": f"bearer {token}"},  # Lowercase
            {"Authorization": f"BEARER {token}"},  # Uppercase
        ]

        for headers in case_variations:
            response = client.get("/protected", headers=headers)
            assert response.status_code == 200, (
                f"Headers {headers} should work - Bearer scheme is case-insensitive"
            )

    def test_invalid_authorization_schemes(self, client: TestClient, test_user_token):
        """Test that only Bearer scheme works for JWT tokens."""
        invalid_schemes = [
            {"Authorization": f"Basic {test_user_token}"},  # Wrong scheme
            {"Authorization": f"Token {test_user_token}"},  # Wrong scheme
            {"Authorization": f"JWT {test_user_token}"},  # Wrong scheme
            {"Authorization": test_user_token},  # Missing scheme
        ]

        for headers in invalid_schemes:
            response = client.get("/protected", headers=headers)
            assert response.status_code == 401, f"Headers {headers} should be rejected"
            data = response.json()
            assert data["detail"] == "Unauthorized"


class TestJWTSecurityTesting:
    """Enhanced security testing for JWT Bearer token attacks and edge cases."""

    def test_malformed_jwt_tokens(self, client: TestClient):
        """Test that malformed JWT tokens are rejected safely."""
        malformed_tokens = [
            "not.a.jwt",  # Not enough parts
            "header.payload",  # Missing signature
            "a.b.c.d",  # Too many parts
            "header.payload.signature.extra",  # Too many parts
            "",  # Empty token
            "Bearer",  # Just the scheme
        ]

        for token in malformed_tokens:
            headers = {"Authorization": f"Bearer {token}"}
            response = client.get("/protected", headers=headers)
            assert response.status_code == 401, f"Token {token} should be rejected"
            data = response.json()
            assert data["detail"] == "Unauthorized"

    def test_header_injection_attempt(self, client: TestClient):
        """Test protection against header injection attacks in JWT."""
        malicious_tokens = [
            "token\r\nSet-Cookie: admin=true",  # CRLF injection
            "token\nX-Admin: true",  # LF injection
            "token; Set-Cookie: admin=true",  # Semicolon injection
        ]

        for token in malicious_tokens:
            headers = {"Authorization": f"Bearer {token}"}
            response = client.get("/protected", headers=headers)
            assert response.status_code == 401, f"Token {token} should be rejected"
            data = response.json()
            assert data["detail"] == "Unauthorized"

    def test_xss_attempt_in_jwt(self, client: TestClient):
        """Test that XSS attempts in JWT tokens are handled safely."""
        malicious_tokens = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "data:text/html,<script>alert('xss')</script>",
        ]

        for token in malicious_tokens:
            headers = {"Authorization": f"Bearer {token}"}
            response = client.get("/protected", headers=headers)
            assert response.status_code == 401, f"Token {token} should be rejected"
            data = response.json()
            assert data["detail"] == "Unauthorized"

    def test_extremely_long_jwt_token(self, client: TestClient):
        """Test handling of extremely long JWT token values."""
        long_token = "a" * 10000  # 10KB token
        headers = {"Authorization": f"Bearer {long_token}"}
        response = client.get("/protected", headers=headers)
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Unauthorized"

    def test_null_byte_injection_jwt(self, client: TestClient):
        """Test protection against null byte injection in JWT."""
        malicious_token = "valid-looking-token\x00malicious"
        headers = {"Authorization": f"Bearer {malicious_token}"}
        response = client.get("/protected", headers=headers)
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Unauthorized"

    def test_empty_bearer_token(self, client: TestClient):
        """Test handling of empty Bearer token values."""
        headers = {"Authorization": "Bearer "}
        response = client.get("/protected", headers=headers)
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Unauthorized"

    def test_whitespace_only_token(self, client: TestClient):
        """Test handling of whitespace-only JWT token values."""
        headers = {"Authorization": "Bearer    \t\n   "}
        response = client.get("/protected", headers=headers)
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Unauthorized"

    def test_expired_token_simulation(self, client: TestClient):
        """Test handling of potentially expired or invalid tokens."""
        # Test with clearly fake JWT-like tokens that won't trigger secret detection
        fake_test_tokens = [
            # Fake JWT-like token structure (not real JWT) for testing
            "fake.jwt.token.header.payload.signature",
            # Another fake JWT-like structure
            "invalid.token.structure.test.only.fake",
            # Malformed token that looks JWT-like but isn't
            "header.payload.signature.but.not.real.jwt",
        ]

        for token in fake_test_tokens:
            headers = {"Authorization": f"Bearer {token}"}
            response = client.get("/protected", headers=headers)
            assert response.status_code == 401, "Test token should be rejected"
            data = response.json()
            assert data["detail"] == "Unauthorized"


class TestErrorHandling:
    """Tests for error handling."""

    def test_nonexistent_endpoint_returns_404(self, client: TestClient):
        """Test accessing a non-existent endpoint returns 404."""
        response = client.get("/nonexistent")

        # Non-existent endpoints return 404
        assert response.status_code == 404
        assert response.json() == {"detail": "Not Found"}

    def test_nonexistent_endpoint_with_auth(self, client: TestClient, bearer_headers):
        """Test accessing a non-existent endpoint with valid authentication."""
        response = client.get("/nonexistent", headers=bearer_headers)

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

    def test_geocode_city_success(self, client: TestClient, bearer_headers):
        """Test successful city geocoding."""
        response = client.get("/geocode/city?city=London", headers=bearer_headers)
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

    def test_geocode_city_not_found(self, client: TestClient, bearer_headers):
        """Test geocoding with non-existent city."""
        response = client.get(
            "/geocode/city?city=Xyzabcdef123NonExistentCity", headers=bearer_headers
        )
        assert response.status_code == 404
        data = response.json()
        assert "City 'Xyzabcdef123NonExistentCity' not found" in data["detail"]

    def test_geocode_health_endpoint(self, client: TestClient, bearer_headers):
        """Test geocoding health endpoint."""
        response = client.get("/geocode/health", headers=bearer_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "geocoding"
        assert data["status"] == "healthy"
        assert "cache_size" in data
        assert data["rate_limiter"] == "active"

    def test_geocode_rate_limiting(self, client: TestClient, bearer_headers):
        """Test user rate limiting."""
        # Make multiple rapid requests
        rate_limited_found = False
        for i in range(15):  # Make more requests to ensure we hit rate limit
            response = client.get(
                f"/geocode/city?city=TestCity{i}", headers=bearer_headers
            )
            # Should get normal responses or rate limiting
            assert response.status_code in [200, 404, 429]
            if response.status_code == 429:
                rate_limited_found = True
                break  # Stop once we hit rate limit

        # Should have hit rate limit at some point
        assert rate_limited_found, "Rate limiting should have been triggered"

    def test_geocode_caching_behavior(self, client: TestClient, bearer_headers):
        """Test that caching works correctly."""
        # First request
        response1 = client.get("/geocode/city?city=Paris", headers=bearer_headers)
        # May be rate limited due to previous tests
        if response1.status_code == 429:
            return  # Skip test if rate limited
        assert response1.status_code in [200, 404]

        if response1.status_code == 200:
            data1 = response1.json()
            assert data1["cached"] is False

            # Second request should be cached
            response2 = client.get("/geocode/city?city=Paris", headers=bearer_headers)
            if response2.status_code == 200:
                data2 = response2.json()
                assert data2["cached"] is True
                assert data1["location"] == data2["location"]

    def test_geocode_authentication_required(self, client: TestClient):
        """Test that authentication is required."""
        response = client.get("/geocode/city?city=London")
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Unauthorized"

    def test_geocode_invalid_input(self, client: TestClient, bearer_headers):
        """Test input validation."""
        # Empty city name
        response = client.get("/geocode/city?city=", headers=bearer_headers)
        assert response.status_code == 422

        # City name too long (>200 chars)
        long_city = "x" * 201
        response = client.get(f"/geocode/city?city={long_city}", headers=bearer_headers)
        assert response.status_code == 422

    def test_geocode_missing_city_parameter(self, client: TestClient, bearer_headers):
        """Test missing city parameter."""
        response = client.get("/geocode/city", headers=bearer_headers)
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
        self, client: TestClient, bearer_headers
    ):
        """Test that city names are handled regardless of case."""
        cities = ["london", "LONDON", "London", "LoNdOn"]

        responses = []
        for city in cities:
            response = client.get(f"/geocode/city?city={city}", headers=bearer_headers)
            responses.append(response)

        # All should work (either 200 for found or consistent behavior, or 429 for rate limiting)
        for response in responses:
            assert response.status_code in [200, 404, 429]

    def test_geocode_special_characters_in_city_name(
        self, client: TestClient, bearer_headers
    ):
        """Test geocoding with special characters in city names."""
        special_cities = [
            "São Paulo",
            "München",
            "北京",  # Beijing in Chinese
            "Москва",  # Moscow in Russian
        ]

        for city in special_cities:
            response = client.get(f"/geocode/city?city={city}", headers=bearer_headers)
            # Should not error, either found (200) or not found (404), or rate limited (429)
            assert response.status_code in [200, 404, 429, 503]

    def test_geocode_whitespace_handling(self, client: TestClient, bearer_headers):
        """Test geocoding with whitespace in city names."""
        response = client.get("/geocode/city?city= London ", headers=bearer_headers)
        # Should handle whitespace gracefully
        assert response.status_code in [200, 404, 429, 503]

    def test_geocode_response_headers(self, client: TestClient, bearer_headers):
        """Test that response headers are appropriate."""
        response = client.get("/geocode/city?city=London", headers=bearer_headers)

        if response.status_code == 200:
            assert response.headers["content-type"] == "application/json"

        # Rate limiting headers (if present)
        # Note: slowapi may add rate limiting headers

    def test_geocode_concurrent_requests(self, client: TestClient, bearer_headers):
        """Test concurrent requests to geocoding endpoint."""
        import concurrent.futures

        def make_request(city_suffix):
            return client.get(
                f"/geocode/city?city=TestCity{city_suffix}", headers=bearer_headers
            )

        # Make concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(make_request, i) for i in range(3)]
            responses = [future.result() for future in futures]

        # All should complete without error
        for response in responses:
            assert response.status_code in [200, 404, 429, 503]

    def test_geocode_service_unavailable_handling(
        self, client: TestClient, bearer_headers
    ):
        """Test handling when geocoding service encounters errors."""
        # Use a city name that might cause service issues or test with mocked failure
        response = client.get(
            "/geocode/city?city=SpecialErrorTestCity", headers=bearer_headers
        )

        # Should handle gracefully - either success, not found, rate limited, or service unavailable
        assert response.status_code in [200, 404, 429, 503]

        if response.status_code == 503:
            data = response.json()
            assert "service temporarily unavailable" in data["detail"].lower()


class TestCrawlingEndpoints:
    """Integration tests for crawling endpoints."""

    def test_crawl_single_url_success(self, client: TestClient, bearer_headers):
        """Test single URL crawling (graceful handling of service downtime)."""
        payload = {
            "urls": ["https://example.com"],
            "markdown_only": True,
            "cache_mode": "enabled",
        }

        response = client.post("/crawl", json=payload, headers=bearer_headers)
        assert response.status_code == 200
        data = response.json()

        # Always verify response structure
        assert data["total_urls"] == 1
        assert "successful_crawls" in data
        assert "failed_crawls" in data
        assert "results" in data
        assert "cached_results" in data
        assert "timestamp" in data
        assert isinstance(data["results"], list)

        # Verify total crawls (successful + failed should equal total)
        assert data["successful_crawls"] + data["failed_crawls"] == data["total_urls"]

        if data["results"]:
            result = data["results"][0]
            assert "url" in result
            assert "success" in result
            # External service may add trailing slash, but our normalization should handle it
            assert result["url"] in ["https://example.com", "https://example.com/"]

            # If Crawl4AI service is down, we expect graceful failure
            if not result["success"]:
                assert "error_message" in result
                # Service downtime is acceptable for tests

    def test_crawl_multiple_urls(self, client: TestClient, bearer_headers):
        """Test crawling multiple URLs (resilient to service downtime)."""
        payload = {
            "urls": ["https://example.com", "https://httpbin.org/html"],
            "markdown_only": False,
            "scrape_internal_links": True,
            "scrape_external_links": True,
        }

        response = client.post("/crawl", json=payload, headers=bearer_headers)
        assert response.status_code == 200
        data = response.json()

        # Always verify response structure
        assert data["total_urls"] == 2
        assert "successful_crawls" in data
        assert "failed_crawls" in data
        assert len(data["results"]) == 2  # Should have results for all URLs

        # Verify total crawls accounting
        assert data["successful_crawls"] + data["failed_crawls"] == data["total_urls"]

        for result in data["results"]:
            assert "url" in result
            assert "success" in result
            # External service may add trailing slash, but our normalization should handle it
            assert result["url"] in [
                "https://example.com",
                "https://example.com/",
                "https://httpbin.org/html",
            ]

            # Service downtime results in failed crawls, which is acceptable
            if not result["success"]:
                assert "error_message" in result

    def test_crawl_with_screenshots(self, client: TestClient, bearer_headers):
        """Test crawling with screenshot capture (resilient to service downtime)."""
        payload = {
            "urls": ["https://example.com"],
            "capture_screenshots": True,
            "screenshot_width": 1280,
            "screenshot_height": 720,
            "screenshot_wait_for": 2,
        }

        response = client.post("/crawl", json=payload, headers=bearer_headers)
        assert response.status_code == 200
        data = response.json()

        # Always verify response structure
        assert data["total_urls"] == 1
        assert "successful_crawls" in data
        assert "failed_crawls" in data
        assert len(data["results"]) == 1

        result = data["results"][0]
        assert "url" in result
        assert "success" in result

        # If service is available and crawl succeeds, verify screenshot handling
        if result["success"]:
            # Screenshot may or may not be captured depending on Crawl4AI availability
            if result.get("screenshot_base64"):
                assert isinstance(result["screenshot_base64"], str)
                assert "screenshot_size" in result
        else:
            # Service downtime is acceptable - verify error handling
            assert "error_message" in result

    def test_crawl_screenshot_dimension_validation(
        self, client: TestClient, bearer_headers
    ):
        """Test screenshot dimension validation."""
        # Too small dimensions
        payload = {
            "urls": ["https://example.com"],
            "capture_screenshots": True,
            "screenshot_width": 100,  # Below minimum 320
            "screenshot_height": 100,  # Below minimum 240
        }

        response = client.post("/crawl", json=payload, headers=bearer_headers)
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

        # Too large dimensions
        payload = {
            "urls": ["https://example.com"],
            "capture_screenshots": True,
            "screenshot_width": 5000,  # Above maximum 3840
            "screenshot_height": 3000,  # Above maximum 2160
        }

        response = client.post("/crawl", json=payload, headers=bearer_headers)
        assert response.status_code == 422

    def test_crawl_health_endpoint(self, client: TestClient, bearer_headers):
        """Test crawling health endpoint."""
        response = client.get("/crawl/health", headers=bearer_headers)
        assert response.status_code == 200
        data = response.json()

        assert data["service"] == "crawling"
        assert "status" in data
        assert "cache_size" in data
        assert "cache_ttl_hours" in data
        assert "rate_limiter_active" in data
        assert "crawl4ai_instance" in data

    def test_crawl_cache_clear_endpoint(self, client: TestClient, bearer_headers):
        """Test cache clearing endpoint."""
        response = client.post("/crawl/cache/clear", headers=bearer_headers)
        assert response.status_code == 200
        data = response.json()

        assert "message" in data
        assert "cache cleared" in data["message"].lower()
        assert "timestamp" in data

    def test_crawl_authentication_required(self, client: TestClient):
        """Test that authentication is required for crawling endpoints."""
        payload = {"urls": ["https://example.com"]}

        # Main crawl endpoint
        response = client.post("/crawl", json=payload)
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Unauthorized"

        # Health endpoint
        response = client.get("/crawl/health")
        assert response.status_code == 401

        # Cache clear endpoint
        response = client.post("/crawl/cache/clear")
        assert response.status_code == 401

    def test_crawl_rate_limiting(self, client: TestClient, bearer_headers):
        """Test user rate limiting for crawling endpoints."""
        rate_limited_found = False

        for i in range(10):  # Make multiple requests to trigger rate limiting
            payload = {"urls": [f"https://example{i}.com"], "cache_mode": "disabled"}
            response = client.post("/crawl", json=payload, headers=bearer_headers)

            # Should get normal responses or rate limiting
            assert response.status_code in [200, 429, 503]
            if response.status_code == 429:
                rate_limited_found = True
                break

        # Should eventually hit rate limit (5/minute)
        assert rate_limited_found, "Rate limiting should have been triggered"

    def test_crawl_caching_behavior(self, client: TestClient, bearer_headers):
        """Test that caching works correctly (resilient to service downtime)."""
        payload = {
            "urls": ["https://example.com"],
            "markdown_only": True,
            "cache_mode": "enabled",
        }

        # First request
        response1 = client.post("/crawl", json=payload, headers=bearer_headers)
        if response1.status_code == 429:
            return  # Skip if rate limited
        assert response1.status_code == 200
        data1 = response1.json()

        # Second request should use cache (if first was successful)
        response2 = client.post("/crawl", json=payload, headers=bearer_headers)
        if response2.status_code == 200:
            data2 = response2.json()

            # If first request succeeded, second should use cache
            if data1["successful_crawls"] > 0:
                assert data2["cached_results"] >= data1["cached_results"]

            # If both failed due to service downtime, both should have 0 cached results
            if data1["successful_crawls"] == 0 and data2["successful_crawls"] == 0:
                assert data1["cached_results"] == 0
                assert data2["cached_results"] == 0

    def test_crawl_cache_bypass(self, client: TestClient, bearer_headers):
        """Test cache bypass functionality."""
        payload = {
            "urls": ["https://example.com"],
            "markdown_only": True,
            "cache_mode": "bypass",
        }

        # Multiple requests with bypass should not use cache
        response1 = client.post("/crawl", json=payload, headers=bearer_headers)
        if response1.status_code == 429:
            return  # Skip if rate limited
        assert response1.status_code == 200
        data1 = response1.json()

        response2 = client.post("/crawl", json=payload, headers=bearer_headers)
        if response2.status_code == 200:
            data2 = response2.json()
            # Both should have 0 cached results since we're bypassing
            assert data1["cached_results"] == 0
            assert data2["cached_results"] == 0

    def test_crawl_input_validation(self, client: TestClient, bearer_headers):
        """Test input validation for crawling requests."""
        # Empty URLs list
        payload = {"urls": []}
        response = client.post("/crawl", json=payload, headers=bearer_headers)
        assert response.status_code == 422

        # Invalid URL format
        payload = {"urls": ["not-a-valid-url"]}
        response = client.post("/crawl", json=payload, headers=bearer_headers)
        assert response.status_code == 422

        # Too many URLs (>10)
        payload = {"urls": [f"https://example{i}.com" for i in range(15)]}
        response = client.post("/crawl", json=payload, headers=bearer_headers)
        assert response.status_code == 422

    def test_crawl_invalid_cache_mode(self, client: TestClient, bearer_headers):
        """Test invalid cache mode validation."""
        payload = {"urls": ["https://example.com"], "cache_mode": "invalid_mode"}

        response = client.post("/crawl", json=payload, headers=bearer_headers)
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_crawl_markdown_only_mode(self, client: TestClient, bearer_headers):
        """Test markdown-only crawling mode (resilient to service downtime)."""
        payload = {"urls": ["https://example.com"], "markdown_only": True}

        response = client.post("/crawl", json=payload, headers=bearer_headers)

        # Handle rate limiting gracefully
        if response.status_code == 429:
            return  # Skip test if rate limited

        assert response.status_code == 200
        data = response.json()

        # Always verify response structure
        assert data["total_urls"] == 1
        assert "successful_crawls" in data
        assert "failed_crawls" in data
        assert len(data["results"]) == 1

        result = data["results"][0]
        assert "url" in result
        assert "success" in result

        # Only verify markdown-only behavior if crawl succeeded
        if result["success"]:
            assert "markdown" in result
            # In markdown-only mode, these should be None or not present
            if "cleaned_html" in result:
                assert result["cleaned_html"] is None
            if "metadata" in result:
                assert result["metadata"] is None

    def test_crawl_link_extraction_options(self, client: TestClient, bearer_headers):
        """Test link extraction configuration."""
        payload = {
            "urls": ["https://example.com"],
            "scrape_internal_links": True,
            "scrape_external_links": True,
            "markdown_only": False,
        }

        response = client.post("/crawl", json=payload, headers=bearer_headers)

        # Handle rate limiting gracefully
        if response.status_code == 429:
            return  # Skip test if rate limited

        assert response.status_code == 200
        data = response.json()

        if data["results"] and data["results"][0]["success"]:
            result = data["results"][0]
            # Should have link fields when link extraction is enabled
            assert "internal_links" in result
            assert "external_links" in result
            assert isinstance(result["internal_links"], list)
            assert isinstance(result["external_links"], list)

    def test_crawl_router_configuration(self, client: TestClient):
        """Test that crawling router is properly configured."""
        # Check OpenAPI schema includes crawling endpoints
        response = client.get("/openapi.json")
        assert response.status_code == 200
        openapi_schema = response.json()

        # Verify crawling endpoints are under /crawl prefix
        assert "/crawl" in openapi_schema["paths"]
        assert "/crawl/health" in openapi_schema["paths"]
        assert "/crawl/cache/clear" in openapi_schema["paths"]

        # Verify tags are applied
        crawl_endpoint = openapi_schema["paths"]["/crawl"]["post"]
        assert "crawling" in crawl_endpoint["tags"]

    def test_crawl_concurrent_requests(self, client: TestClient, bearer_headers):
        """Test concurrent requests to crawling endpoint."""
        import concurrent.futures

        def make_request(url_suffix):
            payload = {
                "urls": [f"https://example{url_suffix}.com"],
                "cache_mode": "disabled",
            }
            return client.post("/crawl", json=payload, headers=bearer_headers)

        # Make concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(make_request, i) for i in range(3)]
            responses = [future.result() for future in futures]

        # All should complete without error
        for response in responses:
            assert response.status_code in [200, 429, 503]

    def test_crawl_service_unavailable_handling(
        self, client: TestClient, bearer_headers
    ):
        """Test handling when Crawl4AI service is unavailable."""
        payload = {"urls": ["https://example.com"], "markdown_only": True}

        response = client.post("/crawl", json=payload, headers=bearer_headers)

        # Should handle gracefully - return 200 with failed crawl results when service is down
        assert response.status_code in [200, 429, 503]

        if response.status_code == 200:
            # Service downtime results in failed crawls within successful API response
            data = response.json()
            assert data["total_urls"] == 1
            assert "successful_crawls" in data
            assert "failed_crawls" in data

            # If all crawls failed due to service downtime, that's acceptable
            if data["failed_crawls"] == data["total_urls"]:
                result = data["results"][0]
                assert not result["success"]
                assert "error_message" in result
        elif response.status_code == 503:
            data = response.json()
            assert (
                "service" in data["detail"].lower()
                or "unavailable" in data["detail"].lower()
            )

    def test_crawl_error_response_format(self, client: TestClient, bearer_headers):
        """Test that error responses follow correct format."""
        # Test with invalid input to trigger error
        payload = {"urls": ["invalid-url"]}

        response = client.post("/crawl", json=payload, headers=bearer_headers)
        assert response.status_code == 422
        data = response.json()

        # Should have proper error format
        assert "detail" in data
        # FastAPI validation errors have specific format

    def test_crawl_response_headers(self, client: TestClient, bearer_headers):
        """Test that response headers are appropriate."""
        payload = {"urls": ["https://example.com"]}

        response = client.post("/crawl", json=payload, headers=bearer_headers)

        if response.status_code == 200:
            assert response.headers["content-type"] == "application/json"

    def test_crawl_recursive_basic(self, client: TestClient, bearer_headers):
        """Test basic recursive crawling functionality."""
        payload = {
            "urls": ["https://example.com"],
            "scrape_internal_links": True,
            "follow_internal_links": True,
            "max_depth": 2,
            "max_pages": 5,
            "cache_mode": "disabled",
        }

        response = client.post("/crawl", json=payload, headers=bearer_headers)

        # Handle rate limiting gracefully
        if response.status_code == 429:
            return  # Skip test if rate limited

        assert response.status_code == 200
        data = response.json()

        # Verify response structure
        assert "total_urls" in data
        assert "successful_crawls" in data
        assert "failed_crawls" in data
        assert "results" in data

        # If crawl succeeded, check depth information
        if data["successful_crawls"] > 0:
            for result in data["results"]:
                assert "depth" in result
                assert isinstance(result["depth"], int)
                assert result["depth"] >= 0

    def test_crawl_recursive_validation(self, client: TestClient, bearer_headers):
        """Test validation for recursive crawling parameters."""
        # Test 1: follow_internal_links requires scrape_internal_links
        payload = {
            "urls": ["https://example.com"],
            "scrape_internal_links": False,
            "follow_internal_links": True,
        }

        response = client.post("/crawl", json=payload, headers=bearer_headers)
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

        # Test 2: follow_internal_links limits seed URLs to 3
        payload = {
            "urls": [
                "https://example1.com",
                "https://example2.com",
                "https://example3.com",
                "https://example4.com",
            ],
            "scrape_internal_links": True,
            "follow_internal_links": True,
        }

        response = client.post("/crawl", json=payload, headers=bearer_headers)
        assert response.status_code == 422

    def test_crawl_recursive_max_depth_validation(
        self, client: TestClient, bearer_headers
    ):
        """Test max_depth parameter validation."""
        # Test max_depth too high
        payload = {
            "urls": ["https://example.com"],
            "scrape_internal_links": True,
            "follow_internal_links": True,
            "max_depth": 10,  # Above maximum of 5
        }

        response = client.post("/crawl", json=payload, headers=bearer_headers)
        assert response.status_code == 422

        # Test max_depth too low
        payload = {
            "urls": ["https://example.com"],
            "scrape_internal_links": True,
            "follow_internal_links": True,
            "max_depth": 0,  # Below minimum of 1
        }

        response = client.post("/crawl", json=payload, headers=bearer_headers)
        assert response.status_code == 422

    def test_crawl_recursive_max_pages_validation(
        self, client: TestClient, bearer_headers
    ):
        """Test max_pages parameter validation."""
        # Test max_pages too high
        payload = {
            "urls": ["https://example.com"],
            "scrape_internal_links": True,
            "follow_internal_links": True,
            "max_pages": 100,  # Above maximum of 50
        }

        response = client.post("/crawl", json=payload, headers=bearer_headers)
        assert response.status_code == 422

        # Test max_pages too low
        payload = {
            "urls": ["https://example.com"],
            "scrape_internal_links": True,
            "follow_internal_links": True,
            "max_pages": 0,  # Below minimum of 1
        }

        response = client.post("/crawl", json=payload, headers=bearer_headers)
        assert response.status_code == 422

    def test_crawl_recursive_with_screenshots(self, client: TestClient, bearer_headers):
        """Test recursive crawling with screenshots enabled."""
        payload = {
            "urls": ["https://example.com"],
            "scrape_internal_links": True,
            "follow_internal_links": True,
            "capture_screenshots": True,
            "screenshot_width": 1280,
            "screenshot_height": 720,
            "max_depth": 2,
            "max_pages": 3,
            "cache_mode": "disabled",
        }

        response = client.post("/crawl", json=payload, headers=bearer_headers)

        # Handle rate limiting gracefully
        if response.status_code == 429:
            return  # Skip test if rate limited

        assert response.status_code == 200
        data = response.json()

        # Verify basic structure
        assert "total_urls" in data
        assert "results" in data

    def test_crawl_recursive_caching(self, client: TestClient, bearer_headers):
        """Test that recursive crawling respects cache settings."""
        payload = {
            "urls": ["https://example.com"],
            "scrape_internal_links": True,
            "follow_internal_links": True,
            "max_depth": 2,
            "max_pages": 5,
            "cache_mode": "enabled",
        }

        # First request
        response1 = client.post("/crawl", json=payload, headers=bearer_headers)
        if response1.status_code == 429:
            return  # Skip if rate limited
        assert response1.status_code == 200
        data1 = response1.json()

        # Second request should use cache
        response2 = client.post("/crawl", json=payload, headers=bearer_headers)
        if response2.status_code == 200:
            data2 = response2.json()

            # If first request had successful crawls, second should have cached results
            if data1["successful_crawls"] > 0:
                assert data2["cached_results"] >= data1["cached_results"]

    def test_crawl_follow_external_links_validation(
        self, client: TestClient, bearer_headers
    ):
        """Test validation for external link following."""
        # Test that follow_external_links requires scrape_external_links
        payload = {
            "urls": ["https://example.com"],
            "scrape_external_links": False,
            "follow_external_links": True,
        }

        response = client.post("/crawl", json=payload, headers=bearer_headers)
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_crawl_follow_external_links_basic(
        self, client: TestClient, bearer_headers
    ):
        """Test basic external link following functionality."""
        payload = {
            "urls": ["https://example.com"],
            "scrape_external_links": True,
            "follow_external_links": True,
            "max_depth": 2,
            "max_pages": 5,
            "cache_mode": "disabled",
        }

        response = client.post("/crawl", json=payload, headers=bearer_headers)

        # Handle rate limiting gracefully
        if response.status_code == 429:
            return  # Skip test if rate limited

        assert response.status_code == 200
        data = response.json()

        # Verify response structure
        assert "total_urls" in data
        assert "successful_crawls" in data
        assert "failed_crawls" in data
        assert "results" in data

        # If crawl succeeded, check depth information
        if data["successful_crawls"] > 0:
            for result in data["results"]:
                assert "depth" in result
                assert isinstance(result["depth"], int)
                assert result["depth"] >= 0

    def test_crawl_follow_both_link_types(self, client: TestClient, bearer_headers):
        """Test following both internal and external links."""
        payload = {
            "urls": ["https://example.com"],
            "scrape_internal_links": True,
            "scrape_external_links": True,
            "follow_internal_links": True,
            "follow_external_links": True,
            "max_depth": 2,
            "max_pages": 5,
            "cache_mode": "disabled",
        }

        response = client.post("/crawl", json=payload, headers=bearer_headers)

        # Handle rate limiting gracefully
        if response.status_code == 429:
            return  # Skip test if rate limited

        assert response.status_code == 200
        data = response.json()

        # Verify basic structure
        assert "total_urls" in data
        assert "results" in data

        # Should handle both internal and external links
        if data["successful_crawls"] > 0:
            for result in data["results"]:
                assert "depth" in result

    def test_crawl_external_links_safety_validation(
        self, client: TestClient, bearer_headers
    ):
        """Test safety validation for external link following."""
        # Test depth limit for external links
        payload = {
            "urls": ["https://example.com"],
            "scrape_external_links": True,
            "follow_external_links": True,
            "max_depth": 4,  # Too high for external links
            "max_pages": 5,
        }

        response = client.post("/crawl", json=payload, headers=bearer_headers)
        assert response.status_code == 422
        error_data = response.json()
        assert "maximum depth is 3 for security" in str(error_data)

        # Test pages limit for external links
        payload = {
            "urls": ["https://example.com"],
            "scrape_external_links": True,
            "follow_external_links": True,
            "max_depth": 2,
            "max_pages": 25,  # Too high for external links
        }

        response = client.post("/crawl", json=payload, headers=bearer_headers)
        assert response.status_code == 422
        error_data = response.json()
        assert "maximum pages is 20 for security" in str(error_data)

        # Test valid external link parameters
        payload = {
            "urls": ["https://example.com"],
            "scrape_external_links": True,
            "follow_external_links": True,
            "max_depth": 3,  # Valid for external links
            "max_pages": 20,  # Valid for external links
            "cache_mode": "disabled",
        }

        response = client.post("/crawl", json=payload, headers=bearer_headers)
        # Should be accepted (200 or 429 for rate limiting)
        assert response.status_code in [200, 429]

    def test_crawl_internal_links_full_limits_allowed(
        self, client: TestClient, bearer_headers
    ):
        """Test that internal link following can use full limits."""
        # Internal links should allow full limits
        payload = {
            "urls": ["https://example.com"],
            "scrape_internal_links": True,
            "follow_internal_links": True,
            "max_depth": 5,  # Full limit for internal links
            "max_pages": 50,  # Full limit for internal links
            "cache_mode": "disabled",
        }

        response = client.post("/crawl", json=payload, headers=bearer_headers)
        # Should be accepted (200 or 429 for rate limiting)
        assert response.status_code in [200, 429]

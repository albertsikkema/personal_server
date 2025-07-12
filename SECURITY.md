# Security Policy

## Secrets Management

This project follows security best practices for managing secrets and credentials:

### Test Environment Secrets

**Test JWT Tokens**: 
- The test files contain well-known example JWT tokens (e.g., "John Doe" tokens) that are commonly used in documentation and testing
- These tokens contain no real secrets - just fake payload data for testing JWT validation
- They are intentionally included to test expired/invalid token handling

**Test Configuration**:
- `JWT_SECRET` in tests uses clearly marked test values like `test-jwt-secret-key-for-testing-purposes-...`
- `API_KEY` in tests uses obvious test values like `test-api-key-12345`
- All test secrets are publicly visible in the repository as they contain no sensitive data

### Production Environment

**Environment Variables**:
- Production secrets are managed via environment variables
- `JWT_SECRET`: Must be a cryptographically secure 32+ character string
- `API_KEY`: Legacy configuration, replaced by JWT authentication
- Never commit real production secrets to the repository

**Required Environment Variables**:
```bash
# Required for JWT authentication
JWT_SECRET=your-secure-production-jwt-secret-minimum-32-characters

# Optional legacy API key (for backward compatibility)
API_KEY=your-production-api-key
```

### GitGuardian Configuration

This repository includes `.gitguardian.yaml` to properly configure secret scanning:
- Test directories are excluded from secret detection
- Known test tokens are whitelisted
- Only production-like secrets in main code trigger alerts

**Note**: During development, an expired test JWT token was accidentally committed to the Bruno API collection. This token has been:
- Removed from the current codebase (replaced with environment variable)
- Added to GitGuardian ignore list (token is expired and non-functional)
- Documented as a learning example for proper secret management

### Security Testing

The test suite includes comprehensive security tests:
- JWT token validation and expiration handling
- Injection attack prevention (XSS, CRLF, null bytes)
- Malformed token handling
- Authentication bypass prevention

### Reporting Security Issues

If you discover a security vulnerability, please report it privately by:
1. Creating a private GitHub security advisory
2. Or emailing the maintainer directly

Please do not create public issues for security vulnerabilities.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Security Features

- **JWT Bearer Token Authentication**: Secure, stateless authentication
- **Rate Limiting**: Protection against brute force attacks
- **Input Validation**: Comprehensive validation using Pydantic
- **CORS Configuration**: Proper cross-origin request handling
- **Security Headers**: Appropriate HTTP security headers
- **SQL Injection Prevention**: Using parameterized queries via SQLAlchemy
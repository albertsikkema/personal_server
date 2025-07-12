"""Authentication backend configuration."""

from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

from config import settings


def get_jwt_strategy() -> JWTStrategy:
    """Get JWT strategy instance.

    Returns:
        JWTStrategy: Configured JWT strategy.
    """
    return JWTStrategy(
        secret=settings.JWT_SECRET,
        lifetime_seconds=settings.JWT_EXPIRE_MINUTES * 60,
        algorithm=settings.JWT_ALGORITHM,
    )


# Configure Bearer token transport
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

# Configure authentication backend
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

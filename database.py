"""Database configuration and session management."""

from collections.abc import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import settings

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    future=True,
)

# Create async session factory
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Metadata for migrations
metadata = MetaData()


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    """Get async database session.

    Yields:
        AsyncSession: Database session for async operations.
    """
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_db_and_tables():
    """Create database tables.

    This function creates all tables defined in the metadata.
    Should be called during application startup.
    """
    from models.user import Base

    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Close database engine.

    Should be called during application shutdown.
    """
    await engine.dispose()

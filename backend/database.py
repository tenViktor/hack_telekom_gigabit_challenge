from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os

# Gets DATABASE_URL from environment variable, falls back to default if not set
# sqlite+aiosqlite:// - Protocol for async SQLite
# ///                - Three slashes for absolute path
# /data/sqlite/app.db - Path inside container (mapped to ./data/sqlite/app.db on host)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:////data/sqlite/app.db")

# Create async engine with SQLite-specific settings
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Print SQL queries (good for debugging)
    future=True,  # Use SQLAlchemy 2.0 features
    connect_args={
        "check_same_thread": False
    },  # Allow SQLite to be used with multiple threads
)

# Create async session factory for database connections
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,  # Don't expire objects after commit
)

# Base class for all database models
Base = declarative_base()


# Database dependency for FastAPI endpoints
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session  # Provide session to endpoint
            await session.commit()  # Commit changes if no exceptions
        except Exception:
            await session.rollback()  # Rollback on error
            raise
        finally:
            await session.close()  # Always close the session

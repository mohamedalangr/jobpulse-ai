"""
Database session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

from src.core.config import settings
from src.core.exceptions import DatabaseConnectionError

logger = logging.getLogger("jobpulse_ai")

try:
    engine = create_engine(
        settings.database_url,
        pool_pre_ping=True,
        echo=settings.debug
    )
except Exception as e:
    logger.error(f"Failed to initialize database engine: {e}")
    raise DatabaseConnectionError(f"Engine initialization failed: {e}")

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    """
    Dependency generator for database sessions.
    Yields a session and ensures it is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

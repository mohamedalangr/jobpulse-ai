import logging
from sqlalchemy import text
from src.database.session import engine

logger = logging.getLogger("jobpulse_ai.database")

def check_connection() -> bool:
    """Test the database connection."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

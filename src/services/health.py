import os
import logging
from dataclasses import dataclass
from src.core.config import settings
from src.core.constants import REQUIRED_DIRECTORIES
from src.database.connection import check_connection

logger = logging.getLogger("jobpulse_ai.health")

@dataclass
class HealthStatus:
    database: bool
    configuration: bool
    logging: bool
    directories: bool

def check_health() -> HealthStatus:
    """
    Check the health of the application's core dependencies.
    """
    # Check configuration
    config_ok = bool(settings.app_name)

    # Check database
    db_ok = check_connection()

    # Check directories
    dirs_ok = True
    for d in REQUIRED_DIRECTORIES:
        if not os.path.exists(d):
            dirs_ok = False
            logger.error(f"Required directory missing: {d}")

    return HealthStatus(
        database=db_ok,
        configuration=config_ok,
        logging=True,
        directories=dirs_ok
    )

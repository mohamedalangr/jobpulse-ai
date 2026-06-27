import os
import sys
import logging
from dataclasses import dataclass
from src.core.config import settings
from src.core.logger import setup_logger
from src.services.health import check_health
from src.core.exceptions import DatabaseConnectionError
from src.core.constants import REQUIRED_DIRECTORIES

@dataclass
class StartupResult:
    configuration_loaded: bool
    logger_initialized: bool
    database_connected: bool

def startup() -> StartupResult:
    """
    Application bootstrap service.
    Initializes core components and verifies system readiness.
    """
    # 1. Initialize logging
    logger = setup_logger("jobpulse_ai")
    logger.info("[startup] Initializing logging")
    
    # 2. Load Configuration
    logger.info("[startup] Loading configuration")
    if not settings.app_name:
        raise ValueError("Configuration failed to load properly.")
    
    # 3. Verify Directories
    logger.info("[startup] Verifying required directories")
    for d in REQUIRED_DIRECTORIES:
        os.makedirs(d, exist_ok=True)

    # 4. Test Database Connection
    logger.info("[database] Testing connection")
    health = check_health()
    if not health.database:
        raise DatabaseConnectionError("Database is not reachable. Check your connection settings.")
    
    logger.info("[startup] Application startup completed")

    return StartupResult(
        configuration_loaded=health.configuration,
        logger_initialized=health.logging,
        database_connected=health.database
    )

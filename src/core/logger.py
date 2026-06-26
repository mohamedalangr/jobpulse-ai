"""
Core logging configuration.
"""
import logging
import sys
from pathlib import Path
from src.core.config import settings

def setup_logger(name: str = __name__) -> logging.Logger:
    logger = logging.getLogger(name)
    
    if logger.hasHandlers():
        return logger

    log_level_attr = getattr(logging, settings.log_level.upper(), logging.INFO)
    logger.setLevel(log_level_attr)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(log_dir / "application.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger("jobpulse_ai")

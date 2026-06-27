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

    import json
    class JsonFormatter(logging.Formatter):
        def format(self, record):
            log_record = {
                "timestamp": self.formatTime(record, self.datefmt),
                "name": record.name,
                "level": record.levelname,
                "message": record.getMessage(),
            }
            # Add any extra attributes added via logging extra={}
            builtin_attrs = {"args", "asctime", "created", "exc_info", "exc_text", "filename", "funcName", "levelname", "levelno", "lineno", "module", "msecs", "message", "msg", "name", "pathname", "process", "processName", "relativeCreated", "stack_info", "thread", "threadName", "taskName"}
            for key, value in record.__dict__.items():
                if key not in builtin_attrs and key not in log_record:
                    log_record[key] = value
            return json.dumps(log_record)

    formatter = JsonFormatter()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(log_dir / "application.log", maxBytes=10*1024*1024, backupCount=5)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger("jobpulse_ai")

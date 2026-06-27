import os
import json
import logging
from datetime import datetime
from typing import Any, List, Union
from src.core.config import settings

logger = logging.getLogger("jobpulse_ai.cache")

class ResponseCache:
    """Saves raw payloads to artifacts/cache/ for offline development and testing."""
    
    def __init__(self, base_dir: str = "artifacts/cache"):
        self.base_dir = base_dir

    def save(self, source_name: str, raw_data: Union[dict, list, str]) -> None:
        if settings.environment != "development":
            return
            
        try:
            source_dir = os.path.join(self.base_dir, source_name.lower())
            os.makedirs(source_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
            filepath = os.path.join(source_dir, f"{timestamp}.json")
            
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(raw_data, f, indent=2, ensure_ascii=False)
                
            logger.info(f"[{source_name}] Cached raw payload to {filepath}")
        except Exception as e:
            logger.warning(f"[{source_name}] Failed to cache response: {e}")

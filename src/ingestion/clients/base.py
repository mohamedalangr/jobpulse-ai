import httpx
import logging
import time
from typing import Any, Dict, Optional
from src.core.exceptions import JobPulseError
from src.core.config import settings

logger = logging.getLogger("jobpulse_ai.clients")

class HttpClientError(JobPulseError):
    pass

class BaseHttpClient:
    """Generic HTTP utility with retries, timeouts, and error handling."""
    def __init__(self, base_url: str = "", timeout: int = 10, max_retries: int = 3):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.headers = {"User-Agent": settings.user_agent}
        self.client = httpx.Client(timeout=self.timeout, headers=self.headers)

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.base_url}{endpoint}"
        for attempt in range(self.max_retries):
            try:
                response = self.client.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.warning(f"HTTP {e.response.status_code} on {url} (Attempt {attempt+1}/{self.max_retries})")
            except httpx.RequestError as e:
                logger.warning(f"Request error on {url}: {e} (Attempt {attempt+1}/{self.max_retries})")
                
            if attempt < self.max_retries - 1:
                delay = 2 ** attempt
                time.sleep(delay)
                
        raise HttpClientError(f"Failed to fetch {url} after {self.max_retries} attempts.")

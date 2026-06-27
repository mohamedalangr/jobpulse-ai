from typing import Dict, List, Optional
from src.ingestion.base import BaseScraper
from src.core.exceptions import DuplicateScraperError
import logging

logger = logging.getLogger("jobpulse_ai.registry")

class SourceRegistry:
    """Registry to manage and track active scraping plugins."""
    
    def __init__(self):
        self._scrapers: Dict[str, BaseScraper] = {}

    def register(self, scraper: BaseScraper, replace: bool = False) -> None:
        """Register a new scraper."""
        source_name = scraper.source_name
        if source_name in self._scrapers and not replace:
            raise DuplicateScraperError(f"Scraper '{source_name}' is already registered. Use replace=True to overwrite.")
            
        self._scrapers[source_name] = scraper
        logger.info(f"Registered scraper: {source_name}")

    def get(self, source_name: str) -> Optional[BaseScraper]:
        """Retrieve a specific scraper."""
        return self._scrapers.get(source_name)

    def unregister(self, source_name: str) -> bool:
        """Remove a scraper from the registry."""
        if source_name in self._scrapers:
            del self._scrapers[source_name]
            logger.info(f"Unregistered scraper: {source_name}")
            return True
        return False

    def get_active_scrapers(self) -> List[BaseScraper]:
        """Return all active scrapers."""
        return list(self._scrapers.values())
    
    @property
    def registered_count(self) -> int:
        """Return the number of registered scrapers."""
        return len(self._scrapers)

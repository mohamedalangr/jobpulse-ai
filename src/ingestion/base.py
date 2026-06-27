"""
Base plugin interface for all scrapers.
"""
from abc import ABC, abstractmethod
from typing import Any, List
import logging

from src.ingestion.domain import JobPosting
from src.core.exceptions import ScrapingError

logger = logging.getLogger("jobpulse_ai.ingestion")

class BaseScraper(ABC):
    """
    Abstract base class that all ingestion sources must implement.
    """
    
    @property
    @abstractmethod
    def source_name(self) -> str:
        """Return the name of the scraping source."""
        pass

    @abstractmethod
    def fetch(self) -> Any:
        """Fetch raw data from the source."""
        pass

    @abstractmethod
    def parse(self, raw_data: Any) -> List[JobPosting]:
        """Parse raw data into a list of standardized JobPosting domain objects."""
        pass

    def run(self) -> List[JobPosting]:
        """
        Orchestrate the scraping process.
        """
        logger.info(f"Starting scraper for source: {self.source_name}")
        try:
            raw_data = self.fetch()
            jobs = self.parse(raw_data)
            logger.info(f"Scraper '{self.source_name}' successfully extracted {len(jobs)} jobs.")
            return jobs
        except Exception as e:
            logger.error(f"Scraper '{self.source_name}' failed: {e}")
            raise ScrapingError(f"Failed to scrape {self.source_name}: {e}")

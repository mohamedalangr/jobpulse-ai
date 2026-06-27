"""
Ingestion Manager for orchestrating multiple scrapers.
"""
import logging
from typing import List

from src.ingestion.base import BaseScraper
from src.ingestion.domain import JobPosting

logger = logging.getLogger("jobpulse_ai.manager")

class IngestionManager:
    """
    Manages the execution of registered scrapers and aggregates their results.
    """
    def __init__(self):
        self.scrapers: List[BaseScraper] = []

    def register_scraper(self, scraper: BaseScraper) -> None:
        """Register a new scraper plugin."""
        self.scrapers.append(scraper)
        logger.info(f"Registered scraper: {scraper.source_name}")

    def run_all(self) -> List[JobPosting]:
        """
        Execute all registered scrapers and combine the results.
        """
        all_jobs: List[JobPosting] = []
        logger.info(f"Starting ingestion process with {len(self.scrapers)} scraper(s).")
        
        for scraper in self.scrapers:
            try:
                jobs = scraper.run()
                all_jobs.extend(jobs)
            except Exception as e:
                # We catch errors here so one failing scraper doesn't crash the entire manager
                logger.error(f"Ingestion Manager caught error from {scraper.source_name}: {e}")
                
        logger.info(f"Ingestion process complete. Total jobs collected: {len(all_jobs)}")
        return all_jobs

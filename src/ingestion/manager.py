from typing import List, Tuple
import logging
from src.domain.entities.job_posting import JobPosting
from src.domain.enums import ScraperStatus
from src.ingestion.registry import SourceRegistry
from src.ingestion.base import ScraperResult

logger = logging.getLogger("jobpulse_ai.manager")

class IngestionManager:
    """Orchestrates scrapers retrieved from the SourceRegistry."""
    
    def __init__(self, registry: SourceRegistry):
        self.registry = registry

    def run_all(self) -> Tuple[List[JobPosting], List[ScraperResult]]:
        """Executes all registered scrapers and aggregates jobs and metrics."""
        active_scrapers = self.registry.get_active_scrapers()
        logger.info(f"Starting ingestion with {len(active_scrapers)} active scraper(s).")
        
        all_jobs: List[JobPosting] = []
        metrics: List[ScraperResult] = []

        for scraper in active_scrapers:
            result = scraper.run()
            metrics.append(result)
            
            if result.status == ScraperStatus.SUCCESS and result.jobs:
                all_jobs.extend(result.jobs)

        logger.info(f"Ingestion complete. Total jobs collected: {len(all_jobs)}")
        return all_jobs, metrics

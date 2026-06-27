import time
from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union
from datetime import datetime, timezone
from dataclasses import dataclass, field
from src.domain.entities.job_posting import JobPosting
from src.domain.enums import ScraperStatus
import logging

logger = logging.getLogger("jobpulse_ai.ingestion")

@dataclass
class ScraperResult:
    source: str
    jobs_collected: int
    duration_seconds: float
    status: ScraperStatus
    started_at: datetime
    finished_at: datetime
    error: str | None = None
    warnings: List[str] = field(default_factory=list)
    jobs: List[JobPosting] = field(default_factory=list)

class BaseParser(ABC):
    """Converts raw fetched content into domain objects."""
    @abstractmethod
    def parse(self, raw_data: Union[bytes, dict, str, List[Any]]) -> List[JobPosting]:
        pass

class BaseScraper(ABC):
    """Abstract base class that defines the contract for every scraper."""
    
    max_retries: int = 3
    retry_delay: int = 2
    
    @property
    @abstractmethod
    def source_name(self) -> str:
        """Return the name of the scraping source."""
        pass
        
    @property
    @abstractmethod
    def parser(self) -> BaseParser:
        """Return the parser used by this scraper."""
        pass

    @abstractmethod
    def fetch(self) -> Union[bytes, dict, str, List[Any]]:
        """Fetch raw data from the source. No DB access."""
        pass

    def run(self) -> ScraperResult:
        """Executes the scraper and returns execution metrics and jobs."""
        logger.info(f"[INGESTION] Source={self.source_name} Status=Started")
        started_at = datetime.now(timezone.utc)
        start_time = time.perf_counter()
        
        raw_data = None
        last_error = None
        for attempt in range(self.max_retries):
            try:
                raw_data = self.fetch()
                break
            except Exception as e:
                last_error = e
                logger.warning(f"[{self.source_name}] Fetch attempt {attempt + 1} failed: {e}")
                time.sleep(self.retry_delay)
                
        if raw_data is None:
            finished_at = datetime.now(timezone.utc)
            duration = time.perf_counter() - start_time
            logger.error(f"[INGESTION] Source={self.source_name} Status=Failed Duration={duration:.2f}s")
            return ScraperResult(
                source=self.source_name,
                jobs_collected=0,
                duration_seconds=duration,
                status=ScraperStatus.FAILED,
                started_at=started_at,
                finished_at=finished_at,
                error=str(last_error)
            )

        try:
            jobs = self.parser.parse(raw_data)
            finished_at = datetime.now(timezone.utc)
            duration = time.perf_counter() - start_time
            logger.info(f"[INGESTION] Source={self.source_name} Jobs={len(jobs)} Duration={duration:.2f}s Status=Success")
            return ScraperResult(
                source=self.source_name,
                jobs_collected=len(jobs),
                duration_seconds=duration,
                status=ScraperStatus.SUCCESS,
                started_at=started_at,
                finished_at=finished_at,
                jobs=jobs
            )
        except Exception as e:
            finished_at = datetime.now(timezone.utc)
            duration = time.perf_counter() - start_time
            logger.error(f"[INGESTION] Source={self.source_name} Status=Failed Duration={duration:.2f}s Error={e}")
            return ScraperResult(
                source=self.source_name,
                jobs_collected=0,
                duration_seconds=duration,
                status=ScraperStatus.FAILED,
                started_at=started_at,
                finished_at=finished_at,
                error=str(e)
            )

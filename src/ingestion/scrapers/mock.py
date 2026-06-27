"""
Mock scraper for testing the ingestion framework.
"""
from typing import Any, List
from datetime import datetime, timezone

from src.ingestion.base import BaseScraper
from src.ingestion.domain import JobPosting

class MockScraper(BaseScraper):
    """
    A mock scraper that returns hardcoded job postings.
    """
    
    @property
    def source_name(self) -> str:
        return "MockSource"

    def fetch(self) -> Any:
        """Mock fetching raw data."""
        return [
            {
                "title": "Senior Data Engineer",
                "company": "Tech Innovations Inc.",
                "location": "Remote",
                "description": "Looking for a seasoned data engineer.",
                "url": "https://mocksource.com/job/1"
            },
            {
                "title": "Machine Learning Scientist",
                "company": "AI Pioneers",
                "location": "San Francisco, CA",
                "description": "Build the future of ML.",
                "url": "https://mocksource.com/job/2"
            }
        ]

    def parse(self, raw_data: Any) -> List[JobPosting]:
        """Mock parsing raw data."""
        jobs = []
        for item in raw_data:
            job = JobPosting(
                title=item["title"],
                company=item["company"],
                location=item["location"],
                description=item["description"],
                source=self.source_name,
                url=item["url"],
                posted_at=datetime.now(timezone.utc)
            )
            jobs.append(job)
        return jobs

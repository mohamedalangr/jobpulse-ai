from typing import Any, List, Union
from datetime import datetime, timezone
import time
from src.domain.entities.job_posting import JobPosting
from src.domain.enums import JobSource, EmploymentType
from src.ingestion.base import BaseScraper, BaseParser

class MockParser(BaseParser):
    def parse(self, raw_data: Union[bytes, dict, str, List[Any]]) -> List[JobPosting]:
        now = datetime.now(timezone.utc)
        jobs = []
        for item in raw_data:
            jobs.append(
                JobPosting(
                    id=item["url"].split("/")[-1],
                    title=item["title"],
                    company=item["company"],
                    description=item["description"],
                    source=JobSource.MOCK.value,
                    url=item["url"],
                    scraped_at=now,
                    raw_data=item,
                    employment_type=EmploymentType.FULL_TIME.value
                )
            )
        return jobs

class MockScraper(BaseScraper):
    """A mock scraper generating realistic domain objects for architecture validation."""
    
    def __init__(self):
        self._parser = MockParser()
        
    @property
    def source_name(self) -> str:
        return JobSource.MOCK.value

    @property
    def parser(self) -> BaseParser:
        return self._parser

    def fetch(self) -> Union[bytes, dict, str, List[Any]]:
        # Simulate network latency
        time.sleep(0.18)
        return [
            {
                "title": f"Data Engineer {i}",
                "company": "Mock Corp",
                "url": f"https://mock.com/job/{i}",
                "description": "Mock description"
            }
            for i in range(1, 9)
        ]

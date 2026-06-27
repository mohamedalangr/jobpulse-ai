from src.ingestion.registry import SourceRegistry
from src.ingestion.manager import IngestionManager
from src.ingestion.scrapers.mock import MockScraper
from src.domain.entities.job_posting import JobPosting
from src.domain.enums import ScraperStatus

def test_ingestion_framework():
    """Verify registry, manager, and mock scraper integration."""
    registry = SourceRegistry()
    mock_scraper = MockScraper()
    registry.register(mock_scraper)
    
    assert registry.registered_count == 1
    assert registry.get_active_scrapers()[0] == mock_scraper
    
    manager = IngestionManager(registry)
    jobs, metrics = manager.run_all()
    
    # Verify Metrics
    assert len(metrics) == 1
    assert metrics[0].status == ScraperStatus.SUCCESS
    assert metrics[0].jobs_collected == 8
    
    # Verify Jobs
    assert len(jobs) == 8
    for job in jobs:
        assert isinstance(job, JobPosting)
        assert job.source == "MOCK"

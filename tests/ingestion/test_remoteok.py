import pytest
from unittest.mock import patch, MagicMock
from src.ingestion.clients.remoteok import RemoteOKClient
from src.ingestion.parsers.remoteok import RemoteOKParser
from src.ingestion.scrapers.remoteok import RemoteOKScraper
from src.domain.enums import ScraperStatus

# Fixture representing a simplified RemoteOK API response
REMOTEOK_FIXTURE = [
    {"legal": "This is a legal disclaimer"},
    {
        "id": "123",
        "position": "Software Engineer",
        "company": "Tech Corp",
        "description": "Great job",
        "url": "https://remoteok.com/job/123",
        "location": "Worldwide",
        "salary_min": 100000,
        "salary_max": 150000
    },
    {
        "id": "124", # Missing position, should be invalid
        "company": "Bad Corp"
    }
]

def test_remoteok_client():
    client = RemoteOKClient()
    with patch("src.ingestion.clients.base.httpx.Client.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = REMOTEOK_FIXTURE
        mock_get.return_value = mock_response
        
        data = client.fetch_jobs()
        assert len(data) == 3
        assert "legal" in data[0]

def test_remoteok_parser():
    parser = RemoteOKParser()
    jobs = parser.parse(REMOTEOK_FIXTURE)
    
    # 3 records: 1 disclaimer (skipped), 1 valid, 1 invalid (skipped)
    assert len(jobs) == 1
    job = jobs[0]
    assert job.title == "Software Engineer"
    assert jobs[0].company == "Tech Corp"
    assert jobs[0].metadata.source == "REMOTEOK"
    assert jobs[0].salary_min == 100000.0

def test_remoteok_scraper_integration():
    scraper = RemoteOKScraper()
    
    # Mock the client fetch so we don't hit the real API
    with patch.object(scraper._client, "fetch_jobs", return_value=REMOTEOK_FIXTURE):
        result = scraper.run()
        assert result.status == ScraperStatus.SUCCESS
        assert result.jobs_collected == 1
        assert len(result.jobs) == 1

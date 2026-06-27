from datetime import datetime, timezone
from src.domain.entities.job_posting import JobPosting
from src.domain.entities.metadata import RecordMetadata

def test_job_posting_creation():
    now = datetime.now(timezone.utc)
    metadata = RecordMetadata(
        source="TEST", 
        pipeline_version="1.0", 
        first_seen_at=now, 
        last_seen_at=now
    )
    job = JobPosting(
        id="123",
        title="Software Engineer",
        company="Tech Corp",
        description="A great job",
        url="https://example.com/job/123",
        raw_data={"test": True},
        metadata=metadata,
        location="Remote",
        salary_min=100000.0,
        salary_max=150000.0
    )
    
    assert job.id == "123"
    assert job.title == "Software Engineer"
    assert job.company == "Tech Corp"
    assert job.metadata.source == "TEST"
    assert job.salary_min == 100000.0
    assert job.salary_max == 150000.0

"""
Tests for the JobPosting domain entity.
"""
from datetime import datetime, timezone
from src.domain.entities.job_posting import JobPosting
from src.domain.enums import EmploymentType, JobSource

def test_job_posting_creation():
    """Test creating a JobPosting with valid required fields."""
    now = datetime.now(timezone.utc)
    raw = {"original_html": "<p>We are hiring!</p>"}
    
    job = JobPosting(
        title="Software Engineer",
        company="Tech Corp",
        description="We are hiring a software engineer.",
        source=JobSource.MOCK.value,
        url="https://mock.com/jobs/1",
        scraped_at=now,
        raw_data=raw
    )
    
    assert job.title == "Software Engineer"
    assert job.company == "Tech Corp"
    assert job.source == "MOCK"
    assert job.scraped_at == now
    assert job.raw_data == raw
    
    # Verify default values
    assert job.id is None
    assert job.location is None
    assert job.skills == []

def test_job_posting_optional_fields():
    """Test creating a JobPosting with optional fields assigned."""
    now = datetime.now(timezone.utc)
    
    job = JobPosting(
        title="Senior Python Developer",
        company="Data LLC",
        description="Write great code.",
        source="REMOTEOK",
        url="https://remoteok.com/job",
        scraped_at=now,
        raw_data={},
        id="12345",
        location="Remote",
        employment_type=EmploymentType.FULL_TIME.value,
        salary_min=120000.0,
        salary_max=150000.0,
        currency="USD",
        skills=["Python", "FastAPI", "SQLAlchemy"]
    )
    
    assert job.id == "12345"
    assert job.location == "Remote"
    assert job.employment_type == "FULL_TIME"
    assert job.salary_min == 120000.0
    assert job.skills == ["Python", "FastAPI", "SQLAlchemy"]

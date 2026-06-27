import pytest
from pathlib import Path
from datetime import datetime, timezone
from src.domain.entities.snapshot import SnapshotScope, SnapshotMetadata
from src.domain.entities.job_posting import JobPosting
from src.domain.entities.metadata import RecordMetadata
from src.intelligence.reporting.snapshot_extractor import SnapshotExtractor
from src.intelligence.reporting.snapshot_serializer import SnapshotSerializer, PyArrowSnapshotBackend

class MockRepository:
    def list(self):
        now = datetime.now(timezone.utc)
        meta = RecordMetadata(source="mock", pipeline_version="1.0", first_seen_at=now, last_seen_at=now)
        return [
            JobPosting(
                id="j1",
                title="Software Engineer",
                company="TechCorp",
                description="Coding",
                url="http://example.com",
                raw_data={},
                metadata=meta,
                skills=["Python", "FastAPI"],
                salary_min=100000,
                salary_max=150000,
                currency="USD",
                posted_at=now
            ),
            JobPosting(
                id="j2",
                title="Data Engineer",
                company="DataCo",
                description="Pipelines",
                url="http://example.com",
                raw_data={},
                metadata=meta,
                skills=["Python", "Spark"],
                posted_at=now
            )
        ]

def test_snapshot_engine_generates_parquet(tmp_path: Path):
    # Setup
    repo = MockRepository()
    extractor = SnapshotExtractor(repo)
    serializer = SnapshotSerializer(base_directory=str(tmp_path))
    
    metadata = SnapshotMetadata(
        snapshot_id="test-123",
        created_at=datetime.now(timezone.utc),
        dataset_version="1.0",
        scope=SnapshotScope.ACTIVE.value,
        record_count=0,
        company_count=0,
        embedding_model="mock",
        ontology_version="mock",
        git_commit="mock",
        schema_version="1.0"
    )
    
    # Execute
    snapshot = serializer.serialize(extractor, metadata)
    
    # Verify Metadata was updated
    assert snapshot.metadata.record_count == 2
    assert snapshot.metadata.company_count == 2
    
    # Verify Streams load correctly from Parquet
    jobs = list(snapshot.jobs())
    assert len(jobs) == 2
    assert jobs[0]["company"] == "TechCorp"
    
    skills = list(snapshot.skills())
    assert len(skills) == 4 # Python, FastAPI, Python, Spark
    
    salaries = list(snapshot.salaries())
    assert len(salaries) == 1
    assert salaries[0]["salary_min"] == 100000
    
    companies = list(snapshot.companies())
    assert len(companies) == 2

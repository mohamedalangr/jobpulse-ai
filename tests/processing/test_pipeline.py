from datetime import datetime
from src.domain.entities.job_posting import JobPosting
from src.domain.entities.metadata import RecordMetadata
from src.processing.pipeline import ProcessingPipeline
from src.processing.stages.validation import ValidationStage
from src.processing.stages.cleaning import CleaningStage
from src.processing.stages.normalization import NormalizationStage
from src.processing.stages.fingerprint import FingerprintStage
from src.processing.stages.deduplication import DeduplicationStage
from src.processing.deduplication.memory_store import MemoryDuplicateStore
from src.processing.deduplication.detector import DuplicateDetector

def test_full_pipeline():
    detector = DuplicateDetector(MemoryDuplicateStore())
    
    pipeline = ProcessingPipeline([
        ValidationStage(),
        CleaningStage(),
        NormalizationStage(),
        FingerprintStage(),
        DeduplicationStage(detector)
    ])
    
    now = datetime.now()
    
    jobs = [
        # Valid job
        JobPosting(
            id="1", title="Software Engineer  ", company="  Tech Corp",
            description="<p>Great job</p>", url="https://mock.com",
            raw_data={}, metadata=RecordMetadata(source="MOCK", pipeline_version="test", first_seen_at=now, last_seen_at=now),
            location="Anywhere", employment_type="full time"
        ),
        # Invalid job (missing title)
        JobPosting(
            id="2", title="", company="Tech Corp", description="",
            url="https://mock.com", raw_data={},
            metadata=RecordMetadata(source="MOCK", pipeline_version="test", first_seen_at=now, last_seen_at=now)
        ),
        # Duplicate of job 1
        JobPosting(
            id="3", title="Software Engineer", company="Tech Corp",
            description="Another desc", url="https://mock.com",
            raw_data={}, metadata=RecordMetadata(source="OTHER", pipeline_version="test", first_seen_at=now, last_seen_at=now)
        )
    ]
    
    processed, report = pipeline.process(jobs)
    
    assert len(processed) == 1
    job = processed[0]
    
    # Check cleaning
    assert job.title == "Software Engineer"
    assert job.company == "Tech Corp"
    assert job.description == "Great job"
    
    # Check normalization
    assert job.location == "Remote"
    assert job.employment_type == "FULL_TIME"
    
    # Check fingerprinting
    assert job.metadata.fingerprint is not None

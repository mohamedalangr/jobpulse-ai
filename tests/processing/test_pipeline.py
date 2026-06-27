from src.domain.entities.job_posting import JobPosting
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
    
    jobs = [
        # Valid job
        JobPosting(
            id="1", title="Software Engineer  ", company="  Tech Corp",
            description="<p>Great job</p>", source="MOCK", url="https://mock.com",
            scraped_at=None, raw_data={}, location="Anywhere", employment_type="full time"
        ),
        # Invalid job (missing title)
        JobPosting(
            id="2", title="", company="Tech Corp", description="",
            source="MOCK", url="https://mock.com", scraped_at=None, raw_data={}
        ),
        # Duplicate of job 1 (same title and company and url)
        JobPosting(
            id="3", title="Software Engineer", company="Tech Corp",
            description="Another desc", source="OTHER", url="https://mock.com",
            scraped_at=None, raw_data={}
        )
    ]
    
    processed = pipeline.process(jobs)
    
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
    assert job.fingerprint is not None

import logging
from typing import List
from src.domain.entities.job_posting import JobPosting
from src.processing.stages.base_stage import PipelineStage
from src.processing.deduplication.detector import DuplicateDetector

logger = logging.getLogger("jobpulse_ai.processing.deduplication")

class DeduplicationStage(PipelineStage):
    """Filters out jobs that trigger the DuplicateDetector."""
    def __init__(self, detector: DuplicateDetector):
        self.detector = detector

    def process(self, jobs: List[JobPosting]) -> List[JobPosting]:
        unique_jobs = []
        for job in jobs:
            if not job.fingerprint:
                # Cannot deduplicate without a fingerprint, so we keep it
                unique_jobs.append(job)
                continue
                
            if self.detector.is_duplicate(job.fingerprint):
                logger.debug(f"Dropped duplicate job: {job.title} at {job.company}")
            else:
                unique_jobs.append(job)
                
        return unique_jobs

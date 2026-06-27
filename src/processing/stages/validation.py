import logging
from typing import List
from src.domain.entities.job_posting import JobPosting
from src.processing.stages.base_stage import PipelineStage

logger = logging.getLogger("jobpulse_ai.processing.validation")

class ValidationStage(PipelineStage):
    """Drops invalid jobs that lack crucial domain identity."""
    def process(self, jobs: List[JobPosting]) -> List[JobPosting]:
        valid_jobs = []
        for job in jobs:
            if not job.id:
                logger.debug("Dropped job missing ID")
                continue
            if not job.title:
                logger.debug(f"Dropped job {job.id} missing title")
                continue
            valid_jobs.append(job)
        return valid_jobs

import hashlib
from typing import List
from src.domain.entities.job_posting import JobPosting
from src.processing.stages.base_stage import PipelineStage

class FingerprintStage(PipelineStage):
    """Generates a stable, cross-source identity hash for deduplication."""
    def process(self, jobs: List[JobPosting]) -> List[JobPosting]:
        for job in jobs:
            title = job.title or ""
            company = job.company or ""
            url = job.url or ""
            
            raw_string = f"{title.lower()}|{company.lower()}|{url.lower()}"
            job.fingerprint = hashlib.sha256(raw_string.encode('utf-8')).hexdigest()
        return jobs

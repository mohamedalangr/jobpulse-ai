import re
from typing import List
from src.domain.entities.job_posting import JobPosting
from src.processing.stages.base_stage import PipelineStage

class CleaningStage(PipelineStage):
    """Cleans up formatting and removes HTML tags."""
    def _process(self, jobs: List[JobPosting]) -> List[JobPosting]:
        for job in jobs:
            if job.title:
                job.title = job.title.strip()
            if job.company:
                job.company = job.company.strip()
            if job.description:
                # Basic HTML stripping using regex for V1
                clean_desc = re.sub(r'<[^>]+>', '', job.description)
                job.description = clean_desc.strip()
        return jobs

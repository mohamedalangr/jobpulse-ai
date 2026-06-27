from typing import List
from src.domain.entities.job_posting import JobPosting
from src.processing.stages.base_stage import PipelineStage

class NormalizationStage(PipelineStage):
    """Normalizes categorical fields to match standard domain taxonomies."""
    def _process(self, jobs: List[JobPosting]) -> List[JobPosting]:
        for job in jobs:
            # Normalize remote location explicitly
            if job.location and job.location.lower() in ["worldwide", "anywhere", "remote"]:
                job.location = "Remote"
            elif not job.location:
                job.location = "Unspecified"
                
            # Normalize employment type
            if job.employment_type:
                job.employment_type = job.employment_type.upper().replace(" ", "_")
        return jobs

from typing import Iterator, Dict, Any
from src.domain.entities.snapshot import SnapshotScope
from src.domain.entities.job_posting import JobPosting

class SnapshotExtractor:
    """
    Extracts raw domain entities from the repository layer and transforms them 
    into dictionary streams optimized for Parquet/Arrow serialization.
    """
    def __init__(self, job_repository: Any):
        self._repo = job_repository

    def _yield_entities(self, scope: str) -> Iterator[JobPosting]:
        # Mocking the repository interaction. In production, this uses 
        # a server-side cursor (e.g. yield_per in SQLAlchemy)
        active_only = (scope == SnapshotScope.ACTIVE.value)
        if hasattr(self._repo, "stream_all"):
            yield from self._repo.stream_all(active_only=active_only)
        else:
            # Fallback for simple mock/test repos
            jobs = self._repo.list() if hasattr(self._repo, "list") else []
            for j in jobs:
                yield j

    def extract_jobs(self, scope: str) -> Iterator[Dict[str, Any]]:
        for job in self._yield_entities(scope):
            yield {
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "country": job.country,
                "employment_type": job.employment_type,
                "experience_level": job.experience_level,
                "posted_at": job.posted_at.isoformat() if job.posted_at else None,
                "source": job.metadata.source if job.metadata else None
            }

    def extract_skills(self, scope: str) -> Iterator[Dict[str, Any]]:
        for job in self._yield_entities(scope):
            for skill in job.skills:
                yield {
                    "job_id": job.id,
                    "skill": skill
                }

    def extract_companies(self, scope: str) -> Iterator[Dict[str, Any]]:
        seen = set()
        for job in self._yield_entities(scope):
            if job.company and job.company not in seen:
                seen.add(job.company)
                yield {
                    "company_name": job.company
                }

    def extract_salaries(self, scope: str) -> Iterator[Dict[str, Any]]:
        for job in self._yield_entities(scope):
            if job.salary_min or job.salary_max:
                yield {
                    "job_id": job.id,
                    "company": job.company,
                    "salary_min": float(job.salary_min) if job.salary_min else None,
                    "salary_max": float(job.salary_max) if job.salary_max else None,
                    "currency": job.currency
                }

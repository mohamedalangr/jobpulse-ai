from typing import Any, List, Dict
from collections import Counter
from src.domain.entities.job_posting import JobPosting
from src.analytics.metrics.base import BaseMetric

class HiringCompaniesMetric(BaseMetric):
    @property
    def name(self) -> str:
        return "hiring_companies"

    def calculate(self, jobs: List[JobPosting]) -> List[Dict[str, Any]]:
        companies = [job.company for job in jobs if job.company]
        counter = Counter(companies)
        return [{"company": k, "count": v} for k, v in counter.most_common(5)]

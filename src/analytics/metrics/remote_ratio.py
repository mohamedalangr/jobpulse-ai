from typing import Any, List
from src.domain.entities.job_posting import JobPosting
from src.analytics.metrics.base import BaseMetric

class RemoteRatioMetric(BaseMetric):
    @property
    def name(self) -> str:
        return "remote_ratio"

    def calculate(self, jobs: List[JobPosting]) -> float:
        if not jobs:
            return 0.0
            
        remote_count = 0
        for job in jobs:
            loc = (job.location or "").lower()
            if "remote" in loc or "anywhere" in loc or "worldwide" in loc:
                remote_count += 1
                
        return float(remote_count / len(jobs))

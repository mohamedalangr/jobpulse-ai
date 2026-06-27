from typing import Any, List
from src.domain.entities.job_posting import JobPosting
from src.analytics.metrics.base import BaseMetric
import statistics

class MedianSalaryMetric(BaseMetric):
    @property
    def name(self) -> str:
        return "median_salary"

    def calculate(self, jobs: List[JobPosting]) -> Any:
        salaries = []
        for job in jobs:
            if job.salary_min and job.salary_max:
                salaries.append((job.salary_min + job.salary_max) / 2)
            elif job.salary_min:
                salaries.append(job.salary_min)
            elif job.salary_max:
                salaries.append(job.salary_max)
                
        if not salaries:
            return 0.0
            
        return float(statistics.median(salaries))

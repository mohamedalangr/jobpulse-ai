from typing import Any, Dict
from src.domain.entities.job_posting import JobPosting
from src.features.base import FeatureExtractor

class SalaryExtractor(FeatureExtractor):
    @property
    def namespace(self) -> str:
        return "salary"

    def extract(self, job: JobPosting) -> Dict[str, Any]:
        has_salary = job.salary_min is not None or job.salary_max is not None
        mean = None
        if has_salary:
            if job.salary_min and job.salary_max:
                mean = (job.salary_min + job.salary_max) / 2
            elif job.salary_min:
                mean = job.salary_min
            else:
                mean = job.salary_max
                
        return {
            "has_salary": has_salary,
            "mean": float(mean) if mean is not None else None,
            "min": float(job.salary_min) if job.salary_min is not None else None,
            "max": float(job.salary_max) if job.salary_max is not None else None,
            "currency": job.currency
        }

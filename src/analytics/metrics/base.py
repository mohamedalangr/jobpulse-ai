from abc import ABC, abstractmethod
from typing import Any, List
from src.domain.entities.job_posting import JobPosting

class BaseMetric(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """The identifier name of the metric (e.g., 'median_salary')."""
        pass

    @abstractmethod
    def calculate(self, jobs: List[JobPosting]) -> Any:
        """Calculates the metric from the job postings."""
        pass

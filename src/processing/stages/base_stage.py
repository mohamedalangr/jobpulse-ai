from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.job_posting import JobPosting

class PipelineStage(ABC):
    """A single stage in the data processing pipeline."""
    @abstractmethod
    def process(self, jobs: List[JobPosting]) -> List[JobPosting]:
        pass

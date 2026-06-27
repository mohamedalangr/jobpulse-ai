from abc import ABC, abstractmethod
from typing import Any, Dict
from src.domain.entities.job_posting import JobPosting

class FeatureExtractor(ABC):
    @property
    @abstractmethod
    def namespace(self) -> str:
        """The namespace prefix for these features (e.g., 'salary')."""
        pass

    @abstractmethod
    def extract(self, job: JobPosting) -> Dict[str, Any]:
        """Extracts features from the job posting. Keys should NOT include the namespace."""
        pass

from abc import ABC, abstractmethod
from typing import Any, List, Union
from src.domain.entities.job_posting import JobPosting

class BaseParser(ABC):
    """Converts raw fetched content into domain objects."""
    @abstractmethod
    def parse(self, raw_data: Union[bytes, dict, str, List[Any]]) -> List[JobPosting]:
        pass

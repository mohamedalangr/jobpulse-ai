from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass
from src.domain.entities.job_posting import JobPosting

@dataclass
class PersistenceReport:
    inserted: int
    updated: int
    unchanged: int
    failed: int
    duration: float

class BaseRepository(ABC):
    @abstractmethod
    def persist(self, jobs: List[JobPosting]) -> PersistenceReport:
        pass

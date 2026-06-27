from abc import ABC, abstractmethod
from typing import List, Tuple
import time
from src.domain.entities.job_posting import JobPosting
from src.processing.metrics import StageResult

class PipelineStage(ABC):
    """A single stage in the data processing pipeline."""
    
    def process(self, jobs: List[JobPosting]) -> Tuple[List[JobPosting], StageResult]:
        start_time = time.perf_counter()
        jobs_in = len(jobs)
        
        result_jobs = self._process(jobs)
        
        duration = time.perf_counter() - start_time
        jobs_out = len(result_jobs)
        
        result = StageResult(
            stage_name=self.__class__.__name__,
            jobs_in=jobs_in,
            jobs_out=jobs_out,
            duration_seconds=duration
        )
        return result_jobs, result

    @abstractmethod
    def _process(self, jobs: List[JobPosting]) -> List[JobPosting]:
        pass

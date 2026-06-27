from dataclasses import dataclass, field
from typing import List

@dataclass
class StageResult:
    stage_name: str
    jobs_in: int
    jobs_out: int
    duration_seconds: float
    warnings: List[str] = field(default_factory=list)

@dataclass
class ProcessingReport:
    input_jobs: int
    output_jobs: int
    stage_reports: List[StageResult]
    total_duration: float

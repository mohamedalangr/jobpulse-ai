from dataclasses import dataclass
from typing import List, Dict, Any
from src.domain.entities.job_posting import JobPosting
from src.analytics.metrics.base import BaseMetric

@dataclass
class AnalyticsReport:
    records_processed: int
    metrics: Dict[str, Any]

class ReportBuilder:
    def __init__(self):
        self._metrics: List[BaseMetric] = []

    def add_metric(self, metric: BaseMetric) -> None:
        self._metrics.append(metric)

    def build(self, jobs: List[JobPosting]) -> AnalyticsReport:
        results = {}
        for metric in self._metrics:
            results[metric.name] = metric.calculate(jobs)
            
        return AnalyticsReport(
            records_processed=len(jobs),
            metrics=results
        )

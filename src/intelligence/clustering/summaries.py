from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ClusterSummary:
    cluster_id: int
    size: int
    median_salary: Optional[float]
    top_companies: List[str]
    top_skills: List[str]
    top_titles: List[str]
    remote_ratio: float
    representative_jobs: List[str] # Titles or brief summaries of nearest points

@dataclass
class ClusterAnalysisReport:
    summaries: List[ClusterSummary]

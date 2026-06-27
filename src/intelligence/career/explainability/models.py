from dataclasses import dataclass
from typing import List, Optional
from src.domain.entities.job_posting import JobPosting

@dataclass
class JobRecommendation:
    job: JobPosting
    similarity_score: float
    transferable_skills: List[str]
    missing_skills: List[str]
    emerging_skills: List[str]
    market_demand_score: str # High, Medium, Low
    salary_delta_pct: Optional[float] # e.g., +18.0
    confidence: float

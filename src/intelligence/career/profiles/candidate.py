from dataclasses import dataclass
from typing import List, Optional, Dict
import numpy as np

@dataclass
class MarketScore:
    overall_score: int # Out of 100
    strengths: List[str]
    weaknesses: List[str]
    readiness_by_role: Dict[str, float] # e.g. {"Senior Backend": 0.83}

@dataclass
class CandidateProfile:
    skills: List[str]
    experience: str
    current_role: Optional[str] = None
    years_experience: Optional[float] = None
    education: Optional[str] = None
    desired_roles: List[str] = None
    preferred_locations: List[str] = None
    preferred_work_mode: Optional[str] = None
    salary_expectation: Optional[float] = None
    embedding: Optional[np.ndarray] = None

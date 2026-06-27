from dataclasses import dataclass
from typing import List, Optional

@dataclass
class CandidateInputDTO:
    skills: List[str]
    experience: str
    current_role: Optional[str] = None
    years_experience: Optional[float] = None
    education: Optional[str] = None
    desired_roles: List[str] = None
    preferred_locations: List[str] = None
    salary_expectation: Optional[float] = None

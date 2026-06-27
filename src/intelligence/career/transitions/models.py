from dataclasses import dataclass
from typing import List

@dataclass
class TransitionEdge:
    from_role: str
    to_role: str
    similarity: float
    salary_delta_pct: float
    required_skills: List[str]
    difficulty: str # Low, Medium, High

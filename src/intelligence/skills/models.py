from dataclasses import dataclass
from typing import Optional

@dataclass
class SkillOccurrence:
    skill: str
    confidence: float
    source: str
    start_offset: Optional[int] = None
    end_offset: Optional[int] = None

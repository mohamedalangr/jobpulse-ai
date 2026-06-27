from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, List, Optional
from src.domain.entities.metadata import RecordMetadata

@dataclass
class JobPosting:
    """
    Pure Python domain object representing a scraped job posting.
    This is the core contract passed between all application layers.
    """
    id: str
    title: str
    company: str
    description: str
    url: str
    raw_data: Any
    metadata: RecordMetadata
    
    location: str | None = None
    country: str | None = None
    employment_type: str | None = None
    experience_level: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    currency: Optional[str] = None
    posted_at: Optional[datetime] = None
    skills: List[str] = field(default_factory=list)

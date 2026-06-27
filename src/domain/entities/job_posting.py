"""
JobPosting domain entity.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any

@dataclass
class JobPosting:
    """
    Pure Python domain object representing a scraped job posting.
    This is the core contract passed between all application layers.
    """
    title: str
    company: str
    description: str
    source: str
    url: str
    scraped_at: datetime
    raw_data: Dict[str, Any]
    
    id: Optional[str] = None
    location: Optional[str] = None
    country: Optional[str] = None
    employment_type: str | None = None
    experience_level: str | None = None
    location: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    fingerprint: str | None = None
    currency: Optional[str] = None
    posted_at: Optional[datetime] = None
    skills: List[str] = field(default_factory=list)

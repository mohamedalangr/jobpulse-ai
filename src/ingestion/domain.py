"""
Domain models for data ingestion.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl

class JobPosting(BaseModel):
    """
    Domain model representing a job posting.
    This is the strongly typed contract between ingestion, processing, and ML layers.
    """
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Hiring company name")
    location: Optional[str] = Field(None, description="Job location")
    description: Optional[str] = Field(None, description="Full job description")
    salary_min: Optional[float] = Field(None, description="Minimum salary")
    salary_max: Optional[float] = Field(None, description="Maximum salary")
    currency: Optional[str] = Field(None, max_length=3, description="3-letter currency code")
    employment_type: Optional[str] = Field(None, description="Employment type (e.g., Full-time, Contract)")
    source: str = Field(..., description="The source scraper name")
    url: HttpUrl = Field(..., description="Original URL of the job posting")
    posted_at: Optional[datetime] = Field(None, description="When the job was originally posted")

"""
Job model definition.
"""
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, Text, DateTime, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base

class Job(Base):
    """
    Job model representing a scraped job posting.
    """
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    company: Mapped[str] = mapped_column(String, index=True)
    location: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    salary_min: Mapped[Optional[float]] = mapped_column(Numeric, nullable=True)
    salary_max: Mapped[Optional[float]] = mapped_column(Numeric, nullable=True)
    currency: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    job_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    source: Mapped[str] = mapped_column(String, index=True)
    url: Mapped[str] = mapped_column(String, unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc)
    )

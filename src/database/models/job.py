"""
Job model definition.
"""
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, Text, DateTime, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector

from src.database.base import Base

class Job(Base):
    """
    Job model representing a scraped job posting.
    """
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source_id: Mapped[str] = mapped_column(String, index=True) # e.g. "10481"
    title: Mapped[str] = mapped_column(String, index=True)
    company: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text)
    url: Mapped[str] = mapped_column(String, nullable=True)
    
    # Optional Source-Owned fields (Layer 1)
    location: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    employment_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    experience_level: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    salary_min: Mapped[Optional[float]] = mapped_column(Numeric, nullable=True)
    salary_max: Mapped[Optional[float]] = mapped_column(Numeric, nullable=True)
    currency: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    
    # Data Lineage Metadata (Layer 2)
    meta_source: Mapped[str] = mapped_column(String, index=True)
    meta_pipeline_version: Mapped[str] = mapped_column(String)
    meta_first_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    meta_last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    meta_processing_duration: Mapped[Optional[float]] = mapped_column(Numeric, nullable=True)
    
    # The crucial unique fingerprint
    fingerprint: Mapped[str] = mapped_column(String, unique=True, index=True)
    
    # Platform-Owned Fields (Layer 3)
    skills: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    raw_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # Vector Embeddings
    embedding: Mapped[Optional[list[float]]] = mapped_column(Vector(384), nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc)
    )

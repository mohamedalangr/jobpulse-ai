import time
import logging
from typing import List
from contextlib import contextmanager
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from src.domain.entities.job_posting import JobPosting
from src.database.models.job import Job
from src.database.repositories.base_repository import BaseRepository, PersistenceReport

logger = logging.getLogger("jobpulse_ai.repository")

class JobRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    @contextmanager
    def transaction(self):
        """Transaction context manager for atomic operations."""
        try:
            yield self
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logger.error(f"Transaction failed, rolled back: {e}")
            raise e

    def persist(self, jobs: List[JobPosting]) -> PersistenceReport:
        start_time = time.perf_counter()
        
        if not jobs:
            return PersistenceReport(0, 0, 0, 0, 0.0)

        failed = 0
        stmt_values = []
        
        for j in jobs:
            if not j.metadata.fingerprint:
                failed += 1
                continue
                
            stmt_values.append({
                "source_id": j.id,
                "title": j.title,
                "company": j.company,
                "description": j.description,
                "url": j.url,
                "location": j.location,
                "country": j.country,
                "employment_type": j.employment_type,
                "experience_level": j.experience_level,
                "salary_min": j.salary_min,
                "salary_max": j.salary_max,
                "currency": j.currency,
                "meta_source": j.metadata.source,
                "meta_pipeline_version": j.metadata.pipeline_version,
                "meta_first_seen_at": j.metadata.first_seen_at,
                "meta_last_seen_at": j.metadata.last_seen_at,
                "meta_processing_duration": j.metadata.processing_duration,
                "fingerprint": j.metadata.fingerprint,
                "raw_data": j.raw_data
            })

        if not stmt_values:
            return PersistenceReport(0, 0, 0, failed, time.perf_counter() - start_time)

        try:
            stmt = insert(Job).values(stmt_values)
            
            # Layer 1 & 2: Update on conflict
            update_dict = {
                "title": stmt.excluded.title,
                "company": stmt.excluded.company,
                "description": stmt.excluded.description,
                "url": stmt.excluded.url,
                "location": stmt.excluded.location,
                "country": stmt.excluded.country,
                "employment_type": stmt.excluded.employment_type,
                "experience_level": stmt.excluded.experience_level,
                "salary_min": stmt.excluded.salary_min,
                "salary_max": stmt.excluded.salary_max,
                "currency": stmt.excluded.currency,
                "raw_data": stmt.excluded.raw_data,
                "meta_last_seen_at": stmt.excluded.meta_last_seen_at,
                "meta_pipeline_version": stmt.excluded.meta_pipeline_version,
                "meta_processing_duration": stmt.excluded.meta_processing_duration,
            }

            upsert_stmt = stmt.on_conflict_do_update(
                index_elements=['fingerprint'],
                set_=update_dict
            )

            result = self.session.execute(upsert_stmt)
            
            # Approximate rowcount for bulk operations
            affected = result.rowcount
            
            duration = time.perf_counter() - start_time
            return PersistenceReport(
                inserted=affected,
                updated=0,
                unchanged=0,
                failed=failed,
                duration=duration
            )

        except Exception as e:
            logger.error(f"Failed to persist batch: {e}")
            raise e

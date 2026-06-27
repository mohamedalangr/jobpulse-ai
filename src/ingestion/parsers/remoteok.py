import logging
from typing import Any, List, Union
from datetime import datetime, timezone
from src.domain.entities.job_posting import JobPosting
from src.domain.entities.metadata import RecordMetadata
from src.domain.enums import JobSource
from src.ingestion.parsers.base import BaseParser

logger = logging.getLogger("jobpulse_ai.parsers.remoteok")

class RemoteOKParser(BaseParser):
    def parse(self, raw_data: Union[bytes, dict, str, List[Any]]) -> List[JobPosting]:
        if not isinstance(raw_data, list):
            logger.error("[REMOTEOK] Expected a list of JSON objects")
            return []

        jobs = []
        invalid_count = 0
        skipped_disclaimer = False
        
        for item in raw_data:
            if not isinstance(item, dict):
                continue
                
            # Skip the legal disclaimer
            if "legal" in item:
                skipped_disclaimer = True
                continue
                
            # Validation Step
            if "id" not in item or "position" not in item or "company" not in item:
                invalid_count += 1
                continue
                
            try:
                # Basic Mapping
                now = datetime.now(timezone.utc)
                metadata = RecordMetadata(
                    source=JobSource.REMOTEOK.value,
                    pipeline_version="0.2.0",
                    first_seen_at=now,
                    last_seen_at=now
                )
                
                job = JobPosting(
                    id=str(item.get("id")),
                    title=item.get("position"),
                    company=item.get("company"),
                    description=item.get("description", ""),
                    url=item.get("url", ""),
                    raw_data=item,
                    metadata=metadata,
                    location=item.get("location"),
                    salary_min=float(item["salary_min"]) if item.get("salary_min") else None,
                    salary_max=float(item["salary_max"]) if item.get("salary_max") else None,
                )
                jobs.append(job)
            except (KeyError, TypeError, ValueError) as e:
                logger.debug(f"[REMOTEOK] Validation error on record: {e}")
                invalid_count += 1

        if skipped_disclaimer:
            logger.info("[REMOTEOK] Disclaimer skipped")
            
        logger.info(f"[REMOTEOK] Parsed: {len(jobs)}")
        if invalid_count > 0:
            logger.warning(f"[REMOTEOK] Invalid: {invalid_count}")
            
        return jobs

from dataclasses import dataclass
from datetime import datetime
from src.domain.enums import JobSource

@dataclass
class RecordMetadata:
    source: JobSource | str
    pipeline_version: str
    first_seen_at: datetime
    last_seen_at: datetime
    fingerprint: str | None = None
    processing_duration: float | None = None

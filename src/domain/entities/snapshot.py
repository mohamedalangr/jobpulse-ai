from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Iterator, Dict, Any, Protocol

class SnapshotScope(Enum):
    ACTIVE = "active"
    ALL = "all"
    CUSTOM = "custom"

@dataclass(frozen=True)
class SnapshotMetadata:
    snapshot_id: str
    created_at: datetime
    dataset_version: str
    scope: str
    record_count: int
    company_count: int
    embedding_model: str
    ontology_version: str
    git_commit: str
    schema_version: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "created_at": self.created_at.isoformat(),
            "dataset_version": self.dataset_version,
            "scope": self.scope,
            "record_count": self.record_count,
            "company_count": self.company_count,
            "embedding_model": self.embedding_model,
            "ontology_version": self.ontology_version,
            "git_commit": self.git_commit,
            "schema_version": self.schema_version
        }

class SnapshotBackend(Protocol):
    """Protocol defining how a snapshot retrieves its underlying projected data streams."""
    def stream_jobs(self) -> Iterator[Dict[str, Any]]: ...
    def stream_skills(self) -> Iterator[Dict[str, Any]]: ...
    def stream_companies(self) -> Iterator[Dict[str, Any]]: ...
    def stream_salaries(self) -> Iterator[Dict[str, Any]]: ...

class MarketSnapshot:
    """
    The canonical representation of the job market at a specific point in time.
    Acts as an Aggregate Root that exposes typed streams of market projections.
    Does not expose raw DataFrames or Parquet specifics.
    """
    def __init__(self, metadata: SnapshotMetadata, backend: SnapshotBackend):
        self._metadata = metadata
        self._backend = backend

    @property
    def metadata(self) -> SnapshotMetadata:
        return self._metadata

    def jobs(self) -> Iterator[Dict[str, Any]]:
        return self._backend.stream_jobs()

    def skills(self) -> Iterator[Dict[str, Any]]:
        return self._backend.stream_skills()

    def companies(self) -> Iterator[Dict[str, Any]]:
        return self._backend.stream_companies()

    def salaries(self) -> Iterator[Dict[str, Any]]:
        return self._backend.stream_salaries()

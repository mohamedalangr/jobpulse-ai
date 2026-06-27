from dataclasses import dataclass
from typing import Any
import uuid
from datetime import datetime
from src.domain.entities.snapshot import SnapshotScope, SnapshotMetadata

@dataclass
class CreateMarketSnapshotCommand:
    scope: SnapshotScope = SnapshotScope.ACTIVE
    dataset_version: str = "1.0.0"

class CreateMarketSnapshotHandler:
    def __init__(self, extractor: Any, serializer: Any):
        self.extractor = extractor
        self.serializer = serializer

    def handle(self, command: CreateMarketSnapshotCommand) -> str:
        snapshot_id = str(uuid.uuid4())
        created_at = datetime.utcnow()
        
        # Define initial metadata
        metadata = SnapshotMetadata(
            snapshot_id=snapshot_id,
            created_at=created_at,
            dataset_version=command.dataset_version,
            scope=command.scope.value,
            record_count=0, # Populated by serializer
            company_count=0, # Populated by serializer
            embedding_model="all-MiniLM-L6-v2",
            ontology_version="v3",
            git_commit="unknown",
            schema_version="1.0"
        )
        
        # Run pipeline
        snapshot = self.serializer.serialize(self.extractor, metadata)
        
        return snapshot.metadata.snapshot_id

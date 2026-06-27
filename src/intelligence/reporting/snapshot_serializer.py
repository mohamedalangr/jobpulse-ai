import os
import json
from datetime import datetime
from pathlib import Path
from typing import Iterator, Dict, Any
import pyarrow as pa
import pyarrow.parquet as pq

from src.domain.entities.snapshot import SnapshotMetadata, MarketSnapshot, SnapshotBackend

class PyArrowSnapshotBackend(SnapshotBackend):
    def __init__(self, base_path: Path):
        self.base_path = base_path
        
    def _read_stream(self, file_name: str) -> Iterator[Dict[str, Any]]:
        filepath = self.base_path / file_name
        if not filepath.exists():
            return
            
        table = pq.read_table(filepath)
        for batch in table.to_batches():
            for row in batch.to_pylist():
                yield row

    def stream_jobs(self) -> Iterator[Dict[str, Any]]:
        yield from self._read_stream("jobs.parquet")

    def stream_skills(self) -> Iterator[Dict[str, Any]]:
        yield from self._read_stream("skills.parquet")

    def stream_companies(self) -> Iterator[Dict[str, Any]]:
        yield from self._read_stream("companies.parquet")

    def stream_salaries(self) -> Iterator[Dict[str, Any]]:
        yield from self._read_stream("salaries.parquet")


class SnapshotSerializer:
    """
    Consumes dictionary streams and serializes them into columnar Parquet files
    using PyArrow. Avoids loading the entire dataset into memory.
    """
    def __init__(self, base_directory: str = "datasets/snapshots"):
        self.base_directory = Path(base_directory)

    def _write_parquet(self, stream: Iterator[Dict[str, Any]], filepath: Path, batch_size: int = 10000) -> int:
        writer = None
        schema = None
        count = 0
        batch = []
        
        for item in stream:
            batch.append(item)
            count += 1
            
            if len(batch) >= batch_size:
                table = pa.Table.from_pylist(batch)
                if writer is None:
                    schema = table.schema
                    writer = pq.ParquetWriter(filepath, schema)
                writer.write_table(table)
                batch.clear()
                
        if batch:
            table = pa.Table.from_pylist(batch)
            if writer is None:
                schema = table.schema
                writer = pq.ParquetWriter(filepath, schema)
            writer.write_table(table)
            
        if writer:
            writer.close()
            
        return count

    def serialize(self, extractor: Any, metadata: SnapshotMetadata) -> MarketSnapshot:
        # Construct directory: YYYY/MM/YYYY-MM-DD/
        date_str = metadata.created_at.strftime("%Y-%m-%d")
        year = metadata.created_at.strftime("%Y")
        month = metadata.created_at.strftime("%m")
        
        target_dir = self.base_directory / year / month / date_str
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract and write streams
        jobs_count = self._write_parquet(extractor.extract_jobs(metadata.scope), target_dir / "jobs.parquet")
        self._write_parquet(extractor.extract_skills(metadata.scope), target_dir / "skills.parquet")
        company_count = self._write_parquet(extractor.extract_companies(metadata.scope), target_dir / "companies.parquet")
        self._write_parquet(extractor.extract_salaries(metadata.scope), target_dir / "salaries.parquet")
        
        # Rebuild metadata with exact counts
        final_metadata = SnapshotMetadata(
            snapshot_id=metadata.snapshot_id,
            created_at=metadata.created_at,
            dataset_version=metadata.dataset_version,
            scope=metadata.scope,
            record_count=jobs_count,
            company_count=company_count,
            embedding_model=metadata.embedding_model,
            ontology_version=metadata.ontology_version,
            git_commit=metadata.git_commit,
            schema_version=metadata.schema_version
        )
        
        with open(target_dir / "manifest.json", "w") as f:
            json.dump(final_metadata.to_dict(), f, indent=2)
            
        backend = PyArrowSnapshotBackend(target_dir)
        return MarketSnapshot(metadata=final_metadata, backend=backend)

import os
import json
from datetime import datetime, timezone
from typing import List
from src.domain.entities.job_posting import JobPosting
from src.features.vector import FeatureVector
from src.export.exporters.base import BaseExporter

class DatasetExporter:
    def __init__(self, export_dir: str, exporters: List[BaseExporter]):
        self.export_dir = export_dir
        self.exporters = exporters
        os.makedirs(self.export_dir, exist_ok=True)

    def export(self, version: str, vectors: List[FeatureVector], jobs: List[JobPosting], pipeline_version: str = "0.3.0") -> None:
        data = []
        for v in vectors:
            row = {
                "job_id": v.job_id,
                "fingerprint": v.fingerprint,
                "version": v.version,
                "extracted_at": v.extracted_at
            }
            row.update(v.features)
            data.append(row)
            
        sources = list(set([j.metadata.source for j in jobs if j.metadata and j.metadata.source]))
        
        base_filename = f"jobs_v{version}"
        for exporter in self.exporters:
            filepath = os.path.join(self.export_dir, base_filename + exporter.extension)
            exporter.export(data, filepath)
            
        manifest = {
            "dataset_version": version,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "record_count": len(vectors),
            "feature_schema": vectors[0].version if vectors else "unknown",
            "pipeline_version": pipeline_version,
            "sources": sources
        }
        
        manifest_path = os.path.join(self.export_dir, "manifest.json")
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)

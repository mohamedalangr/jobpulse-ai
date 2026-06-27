import os
from src.ingestion.manager import IngestionManager
from src.ingestion.scrapers.remoteok import RemoteOKScraper
from src.ingestion.registry import SourceRegistry
from src.processing.pipeline import ProcessingPipeline
from src.processing.stages.validation import ValidationStage
from src.processing.stages.cleaning import CleaningStage
from src.processing.stages.normalization import NormalizationStage
from src.processing.stages.fingerprint import FingerprintStage
from src.processing.stages.deduplication import DeduplicationStage
from src.processing.deduplication.memory_store import MemoryDuplicateStore
from src.processing.deduplication.detector import DuplicateDetector

from src.features.registry import FeatureRegistry
from src.analytics.report_builder import ReportBuilder
from src.analytics.metrics.median_salary import MedianSalaryMetric
from src.analytics.metrics.top_skills import TopSkillsMetric
from src.analytics.metrics.remote_ratio import RemoteRatioMetric
from src.analytics.metrics.hiring_companies import HiringCompaniesMetric

from src.export.dataset_exporter import DatasetExporter
from src.export.exporters.csv import CSVExporter
from src.export.exporters.json import JSONExporter
from src.export.exporters.parquet import ParquetExporter

def main():
    print("=" * 41)
    print("JobPulse AI Analytics Engine Demo")
    print("=" * 41)
    
    registry = SourceRegistry()
    registry.register(RemoteOKScraper())
    manager = IngestionManager(registry)
    jobs, _ = manager.run_all()
    
    detector = DuplicateDetector(MemoryDuplicateStore())
    pipeline = ProcessingPipeline([
        ValidationStage(),
        CleaningStage(),
        NormalizationStage(),
        FingerprintStage(),
        DeduplicationStage(detector)
    ])
    processed_jobs, report = pipeline.process(jobs)
    
    feature_registry = FeatureRegistry(version="v1")
    feature_registry.discover("src.features.extractors")
    vectors = feature_registry.extract_all(processed_jobs)
    
    builder = ReportBuilder()
    builder.add_metric(MedianSalaryMetric())
    builder.add_metric(TopSkillsMetric())
    builder.add_metric(RemoteRatioMetric())
    builder.add_metric(HiringCompaniesMetric())
    analytics = builder.build(processed_jobs)
    
    export_dir = os.path.join(os.getcwd(), "datasets", "processed")
    exporter = DatasetExporter(
        export_dir=export_dir,
        exporters=[CSVExporter(), JSONExporter(), ParquetExporter()]
    )
    exporter.export(version="1.0", vectors=vectors, jobs=processed_jobs, pipeline_version="0.3.0")
    
    print("\n=========================================")
    print("JobPulse AI Analytics Report")
    print("=========================================")
    print(f"\nRecords Processed: {analytics.records_processed:,}")
    
    median = analytics.metrics.get("median_salary", 0.0)
    print(f"\nMedian Salary: ${median:,.0f}")
    
    remote_ratio = analytics.metrics.get("remote_ratio", 0.0)
    print(f"\nRemote Jobs: {int(remote_ratio * 100)}%")
    
    top_skills = analytics.metrics.get("top_skills", [])
    print("\nTop Skills:")
    for i, s in enumerate(top_skills, 1):
        print(f"{i}. {s['skill'].capitalize()}")
        
    companies = analytics.metrics.get("hiring_companies", [])
    print("\nTop Hiring Companies:")
    for i, c in enumerate(companies, 1):
        print(f"{i}. {c['company']}")
        
    print(f"\nFeature Vectors Generated: {len(vectors):,}")
    
    print("\nDatasets Exported:")
    print("* jobs_v1.0.parquet")
    print("* jobs_v1.0.csv")
    print("* jobs_v1.0.json")
    print("* manifest.json")

if __name__ == "__main__":
    main()

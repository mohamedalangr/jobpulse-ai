import sys
from src.core.config import settings
from src.core.logger import setup_logger
from src.ingestion.registry import SourceRegistry
from src.ingestion.manager import IngestionManager
from src.ingestion.scrapers.remoteok import RemoteOKScraper

def main():
    setup_logger("jobpulse_ai")
    
    print("=" * 41)
    print("RemoteOK Ingestion")
    print("=" * 41)
    
    registry = SourceRegistry()
    registry.register(RemoteOKScraper())
    
    manager = IngestionManager(registry)
    
    jobs, metrics = manager.run_all()
    
    metric = metrics[0] if metrics else None
    
    if metric:
        print(f"\nJobs Retrieved: {metric.raw_records}")
        print(f"Parsed Successfully: {metric.jobs_collected}")
        print(f"Failed Records: {metric.failed_records}")
        print(f"Execution Time: {metric.duration_seconds:.2f} s\n")
    else:
        print("\nIngestion failed.\n")
        return

    print("=" * 41)
    print("Processing Pipeline")
    print("=" * 41)
    
    from src.processing.pipeline import ProcessingPipeline
    from src.processing.stages.validation import ValidationStage
    from src.processing.stages.cleaning import CleaningStage
    from src.processing.stages.normalization import NormalizationStage
    from src.processing.stages.fingerprint import FingerprintStage
    from src.processing.stages.deduplication import DeduplicationStage
    from src.processing.deduplication.memory_store import MemoryDuplicateStore
    from src.processing.deduplication.detector import DuplicateDetector
    
    detector = DuplicateDetector(MemoryDuplicateStore())
    pipeline = ProcessingPipeline([
        ValidationStage(),
        CleaningStage(),
        NormalizationStage(),
        FingerprintStage(),
        DeduplicationStage(detector)
    ])
    
    processed_jobs = pipeline.process(jobs)
    print(f"\nFinal Processed Jobs: {len(processed_jobs)}\n")

if __name__ == "__main__":
    main()

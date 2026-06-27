import sys
import os
import asyncio
from datetime import datetime, timezone

# Ensure src is in PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.core.config import settings
from src.core.logger import setup_logger
from src.ingestion.registry import SourceRegistry
from src.ingestion.manager import IngestionManager
from src.ingestion.scrapers.remoteok import RemoteOKScraper
from src.processing.pipeline import ProcessingPipeline
from src.processing.stages.cleaning import CleaningStage
from src.processing.stages.normalization import NormalizationStage
from src.processing.stages.fingerprint import FingerprintStage
from src.processing.stages.deduplication import DeduplicationStage
from src.processing.stages.validation import ValidationStage
from src.database.session import SessionLocal
from src.database.uow import SQLAlchemyUnitOfWork
from src.application.context import RequestContext

def main():
    setup_logger("jobpulse_ai")
    print("=========================================")
    print(" JobPulse AI - Seed Database Pipeline")
    print("=========================================")
    
    # 1. Setup Ingestion (Real Adapters)
    registry = SourceRegistry()
    registry.register(RemoteOKScraper())
    manager = IngestionManager(registry)
    
    print("\n[1/4] Running Ingestion...")
    raw_jobs, metrics = manager.run_all()
    print(f"Ingested {len(raw_jobs)} raw jobs.")
    
    if not raw_jobs:
        print("No jobs fetched. Exiting.")
        return

    # 2. Setup Processing Pipeline
    pipeline = ProcessingPipeline([
        CleaningStage(),
        NormalizationStage(),
        FingerprintStage(),
        DeduplicationStage(),
        ValidationStage()
    ])
    
    print("\n[2/4] Running Processing Pipeline...")
    processed_jobs, proc_metrics = pipeline.process(raw_jobs)
    print(f"Processed {len(processed_jobs)} valid jobs.")
    
    if not processed_jobs:
        print("No valid jobs after processing. Exiting.")
        return

    # 3. Save to Database
    print("\n[3/4] Persisting to PostgreSQL...")
    uow = SQLAlchemyUnitOfWork(SessionLocal)
    context = RequestContext(correlation_id="seed_script", principal_id="system")
    
    with uow:
        for job in processed_jobs:
            uow.jobs.add(job)
        uow.commit()
    print(f"Persisted {len(processed_jobs)} jobs.")

    # 4. Trigger Snapshots & Trends (Placeholder for RC-03 / RC-04 full integration)
    print("\n[4/4] Pipeline Complete. Data is ready for analysis.")
    print("Run `python ops/scripts/generate_snapshot.py` to compute market trends.")

if __name__ == "__main__":
    main()

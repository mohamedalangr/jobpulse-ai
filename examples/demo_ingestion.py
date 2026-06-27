import sys
from src.core.config import settings
from src.core.logger import setup_logger
from src.ingestion.registry import SourceRegistry
from src.ingestion.manager import IngestionManager
from src.ingestion.scrapers.mock import MockScraper

def main():
    setup_logger("jobpulse_ai")
    
    print("=" * 41)
    print(f"{settings.app_name} - Ingestion Demo")
    print("=" * 41)
    
    # 1. Setup Registry
    registry = SourceRegistry()
    registry.register(MockScraper())
    
    print(f"\nRegistered Sources: {registry.registered_count}")
    
    # 2. Setup Manager
    manager = IngestionManager(registry)
    
    # 3. Execute
    for scraper in registry.get_active_scrapers():
        print(f"Running {scraper.__class__.__name__}...")
        
    jobs, metrics = manager.run_all()
    
    for metric in metrics:
        print(f"Collected Jobs: {metric.jobs_collected}")
        print(f"Execution Time: {metric.duration_seconds:.2f} s")
    
    print("\nIngestion completed successfully.")

if __name__ == "__main__":
    main()

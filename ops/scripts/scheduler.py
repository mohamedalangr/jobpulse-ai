import os
import sys
import time
import schedule
import subprocess
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.core.logger import setup_logger

logger = logging.getLogger("jobpulse_ai.scheduler")

def run_ingestion():
    logger.info("Starting scheduled ingestion...")
    try:
        subprocess.run(["python", "ops/scripts/seed_database.py"], check=True)
        logger.info("Scheduled ingestion completed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Scheduled ingestion failed: {e}")

def main():
    setup_logger("jobpulse_ai")
    logger.info("Starting JobPulse AI Scheduler...")
    
    # Run ingestion every day at 02:00 AM
    schedule.every().day.at("02:00").do(run_ingestion)
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()

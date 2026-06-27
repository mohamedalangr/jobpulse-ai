import logging
from typing import List
from src.domain.entities.job_posting import JobPosting
from src.processing.stages.base_stage import PipelineStage

logger = logging.getLogger("jobpulse_ai.processing")

class ProcessingPipeline:
    """Orchestrates the sequential execution of PipelineStages."""
    def __init__(self, stages: List[PipelineStage]):
        self.stages = stages

    def process(self, jobs: List[JobPosting]) -> List[JobPosting]:
        logger.info(f"Starting processing pipeline with {len(jobs)} jobs")
        
        current_jobs = jobs
        for stage in self.stages:
            stage_name = stage.__class__.__name__
            logger.info(f"Running stage: {stage_name}")
            current_jobs = stage.process(current_jobs)
            logger.info(f"Stage {stage_name} completed, {len(current_jobs)} jobs remaining")
            
            if not current_jobs:
                logger.warning("No jobs remaining, aborting pipeline")
                break
                
        logger.info(f"Processing pipeline complete. Final jobs: {len(current_jobs)}")
        return current_jobs

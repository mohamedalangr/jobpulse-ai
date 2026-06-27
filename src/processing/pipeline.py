import time
import logging
from typing import List, Tuple
from src.domain.entities.job_posting import JobPosting
from src.processing.stages.base_stage import PipelineStage
from src.processing.metrics import ProcessingReport

logger = logging.getLogger("jobpulse_ai.processing")

class ProcessingPipeline:
    """Orchestrates the sequential execution of PipelineStages."""
    def __init__(self, stages: List[PipelineStage]):
        self.stages = stages

    def process(self, jobs: List[JobPosting]) -> Tuple[List[JobPosting], ProcessingReport]:
        logger.info(f"Starting processing pipeline with {len(jobs)} jobs")
        start_time = time.perf_counter()
        input_jobs = len(jobs)
        
        current_jobs = jobs
        stage_reports = []
        
        for stage in self.stages:
            stage_name = stage.__class__.__name__
            current_jobs, result = stage.process(current_jobs)
            stage_reports.append(result)
            
            logger.info(f"Stage {stage_name}: {result.jobs_in} -> {result.jobs_out} ({result.duration_seconds:.4f}s)")
            
            if not current_jobs:
                logger.warning("No jobs remaining, aborting pipeline")
                break
                
        total_duration = time.perf_counter() - start_time
        report = ProcessingReport(
            input_jobs=input_jobs,
            output_jobs=len(current_jobs),
            stage_reports=stage_reports,
            total_duration=total_duration
        )
        
        logger.info(f"Processing complete. Final jobs: {report.output_jobs} in {report.total_duration:.2f}s")
        return current_jobs, report

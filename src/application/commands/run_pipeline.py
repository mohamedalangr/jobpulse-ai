from dataclasses import dataclass
from src.application.commands.base import CommandHandler
from src.application.context import RequestContext
from src.application.events.events import PipelineCompletedEvent

@dataclass
class RunPipelineCommand:
    source_name: str = "all"
    force_rebuild_embeddings: bool = False

class RunPipelineUseCase(CommandHandler):
    def __init__(self, publisher, ingestion_manager, pipeline, vector_store, embedding_cache):
        super().__init__(publisher)
        self.manager = ingestion_manager
        self.pipeline = pipeline
        self.vector_store = vector_store
        self.embedding_cache = embedding_cache

    def execute(self, command: RunPipelineCommand, context: RequestContext) -> int:
        if command.source_name == "all":
            raw_jobs, _ = self.manager.run_all()
        else:
            raw_jobs = self.manager.run(command.source_name)
            
        processed_jobs, _ = self.pipeline.process(raw_jobs)
        
        self.publisher.publish(PipelineCompletedEvent(
            correlation_id=context.correlation_id,
            jobs_processed=len(processed_jobs)
        ))
        
        return len(processed_jobs)

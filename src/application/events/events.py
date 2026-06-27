from dataclasses import dataclass
from src.application.events.base import Event

@dataclass
class PipelineCompletedEvent(Event):
    jobs_processed: int = 0
    duration_seconds: float = 0.0

@dataclass
class EmbeddingGeneratedEvent(Event):
    model_name: str = ""
    vectors_computed: int = 0
    
@dataclass
class LearningPlanGeneratedEvent(Event):
    candidate_role: str = ""
    target_salary_gain: float = 0.0

from dataclasses import dataclass
from typing import List
from src.intelligence.career.explainability.models import JobRecommendation
from src.intelligence.career.transitions.models import TransitionEdge
from src.intelligence.career.insights.models import CareerInsights
from src.intelligence.career.evaluation.models import RecommendationEvaluation

@dataclass
class RecommendationResult:
    recommendations: List[JobRecommendation]
    transition_path: List[TransitionEdge]
    insights: CareerInsights
    evaluation: RecommendationEvaluation

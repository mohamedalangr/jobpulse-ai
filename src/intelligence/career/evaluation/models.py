from dataclasses import dataclass

@dataclass
class RecommendationEvaluation:
    average_similarity: float
    average_learning_gap: float
    average_salary_delta_pct: float
    coverage: float
    recommendation_diversity: float

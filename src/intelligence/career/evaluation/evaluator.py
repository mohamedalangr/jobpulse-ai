from typing import List
from src.intelligence.career.explainability.models import JobRecommendation
from src.intelligence.career.evaluation.models import RecommendationEvaluation

class RecommendationEvaluator:
    def evaluate(self, recommendations: List[JobRecommendation], total_jobs_in_db: int) -> RecommendationEvaluation:
        if not recommendations:
            return RecommendationEvaluation(0.0, 0.0, 0.0, 0.0, 0.0)
            
        avg_sim = sum(r.similarity_score for r in recommendations) / len(recommendations)
        
        avg_missing = sum(len(r.missing_skills) for r in recommendations) / len(recommendations)
        
        valid_salaries = [r.salary_delta_pct for r in recommendations if r.salary_delta_pct is not None]
        avg_salary = sum(valid_salaries) / len(valid_salaries) if valid_salaries else 0.0
        
        coverage = len(recommendations) / total_jobs_in_db if total_jobs_in_db > 0 else 0.0
        
        unique_titles = len(set(r.job.title for r in recommendations if r.job.title))
        diversity = unique_titles / len(recommendations) if recommendations else 0.0
        
        return RecommendationEvaluation(
            average_similarity=round(avg_sim, 3),
            average_learning_gap=round(avg_missing, 1),
            average_salary_delta_pct=round(avg_salary, 1),
            coverage=round(coverage, 4),
            recommendation_diversity=round(diversity, 2)
        )

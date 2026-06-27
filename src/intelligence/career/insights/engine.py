from typing import List
from collections import Counter
from src.intelligence.career.explainability.models import JobRecommendation
from src.intelligence.career.insights.models import CareerInsights
from src.intelligence.career.transitions.models import TransitionEdge

class CareerInsightsEngine:
    def generate(self, recommendations: List[JobRecommendation], edges: List[TransitionEdge]) -> CareerInsights:
        if not recommendations:
            return CareerInsights("Unknown", 0.0, "Unknown", 0.0, "Unknown", "Unknown")
            
        all_skills = []
        for r in recommendations:
            all_skills.extend(r.transferable_skills + r.missing_skills)
            
        if all_skills:
            most_valuable = Counter(all_skills).most_common(1)[0][0]
            prevalence = sum(1 for r in recommendations if most_valuable in (r.transferable_skills + r.missing_skills)) / len(recommendations)
        else:
            most_valuable = "Unknown"
            prevalence = 0.0
            
        highest_salary_rec = max(recommendations, key=lambda r: r.salary_delta_pct or -999.0)
        highest_salary_pct = highest_salary_rec.salary_delta_pct or 0.0
        highest_salary_role = highest_salary_rec.job.title or "Unknown Role"
        
        if edges:
            fastest_edge = min(edges, key=lambda e: len(e.required_skills))
            fastest_role = fastest_edge.to_role
            fastest_gap = fastest_edge.difficulty
        else:
            fastest_role = "Unknown"
            fastest_gap = "Unknown"
            
        return CareerInsights(
            most_valuable_skill=most_valuable,
            most_valuable_skill_prevalence=round(prevalence, 2),
            highest_salary_increase_role=highest_salary_role,
            highest_salary_increase_pct=highest_salary_pct,
            fastest_transition_role=fastest_role,
            fastest_transition_gap=fastest_gap
        )

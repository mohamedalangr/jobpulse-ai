from typing import List, Dict
from src.intelligence.career.explainability.models import JobRecommendation
from src.intelligence.learning.models import SkillROI
from src.intelligence.learning.graph import LearningGraph

class SkillPrioritizer:
    def __init__(self, graph: LearningGraph):
        self.graph = graph

    def prioritize(self, recommendations: List[JobRecommendation]) -> List[SkillROI]:
        skill_stats = {}
        
        for rec in recommendations:
            for skill in rec.missing_skills:
                skill_lower = skill.lower()
                if skill_lower not in skill_stats:
                    skill_stats[skill_lower] = {"count": 0, "salary_sum": 0.0, "salary_count": 0, "name": skill}
                
                skill_stats[skill_lower]["count"] += 1
                if rec.salary_delta_pct is not None:
                    skill_stats[skill_lower]["salary_sum"] += rec.salary_delta_pct
                    skill_stats[skill_lower]["salary_count"] += 1
                    
        total_recs = len(recommendations) if recommendations else 1
        
        rois = []
        for s_lower, stats in skill_stats.items():
            demand = stats["count"] / total_recs
            salary_impact = stats["salary_sum"] / stats["salary_count"] if stats["salary_count"] > 0 else 0.0
            
            node = self.graph.get_node(s_lower)
            cost = node.estimated_hours if node else 20.0
            base_demand = node.demand_weight if node else 0.5
            
            blended_demand = (demand * 0.7) + (base_demand * 0.3)
            norm_salary = max(0.1, min(max(salary_impact, 0) / 50.0, 1.0))
            transition_unlock = stats["count"]
            gap = 1.0
            
            score = (blended_demand * norm_salary * transition_unlock * gap) / max(cost, 1.0)
            
            if score > 0.5: rating = "Excellent"
            elif score > 0.2: rating = "Good"
            else: rating = "Fair"
            
            rois.append(SkillROI(
                skill=stats["name"],
                learning_time_hours=cost,
                jobs_unlocked=transition_unlock,
                salary_gain_pct=round(salary_impact, 1),
                roi_score=round(score, 3),
                roi_rating=rating
            ))
            
        rois.sort(key=lambda x: x.roi_score, reverse=True)
        return rois

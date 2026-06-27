from src.intelligence.learning.models import LearningPlan, LearningPlanEvaluation

class LearningEvaluator:
    def evaluate(self, plan: LearningPlan) -> LearningPlanEvaluation:
        if not plan.skill_rois:
            return LearningPlanEvaluation(0.0, 0.0, 0.0, 0.0, 0.0)
            
        avg_sal = sum(r.salary_gain_pct for r in plan.skill_rois) / len(plan.skill_rois)
        avg_unlocked = sum(r.jobs_unlocked for r in plan.skill_rois) / len(plan.skill_rois)
        avg_hrs = sum(r.learning_time_hours for r in plan.skill_rois) / len(plan.skill_rois)
        
        sim_gain = 0.0
        if len(plan.simulations) >= 2:
            sim_gain = plan.simulations[-1].average_similarity - plan.simulations[0].average_similarity
            
        roi_score = (avg_sal * avg_unlocked) / max(avg_hrs, 1.0)
        
        return LearningPlanEvaluation(
            average_salary_gain=round(avg_sal, 1),
            average_similarity_gain=round(sim_gain, 3),
            average_jobs_unlocked=round(avg_unlocked, 1),
            average_learning_hours=round(avg_hrs, 1),
            roi_score=round(roi_score, 2)
        )

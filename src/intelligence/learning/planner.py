from typing import List
from src.intelligence.career.profiles.candidate import CandidateProfile
from src.intelligence.career.explainability.models import JobRecommendation
from src.intelligence.learning.models import LearningPlan, SimulationState
from src.intelligence.learning.prioritizer import SkillPrioritizer
from src.intelligence.learning.impact import LearningImpactEngine
from src.intelligence.learning.curriculum import CurriculumGenerator
from src.intelligence.learning.synergy import SkillSynergyAnalyzer
from src.intelligence.learning.evaluation import LearningEvaluator

class LearningPlanner:
    def __init__(self, prioritizer: SkillPrioritizer, impact_engine: LearningImpactEngine, 
                 curriculum_gen: CurriculumGenerator, synergy_analyzer: SkillSynergyAnalyzer,
                 evaluator: LearningEvaluator):
        self.prioritizer = prioritizer
        self.impact_engine = impact_engine
        self.curriculum_gen = curriculum_gen
        self.synergy_analyzer = synergy_analyzer
        self.evaluator = evaluator

    def generate_plan(self, candidate: CandidateProfile, initial_recommendations: List[JobRecommendation]) -> LearningPlan:
        # 1. Prioritize Skills
        rois = self.prioritizer.prioritize(initial_recommendations)
        
        # 2. Base Simulation
        base_state = self.impact_engine._build_state("Current Profile", [], initial_recommendations)
        simulations = [base_state]
        
        # 3. Iterative Impact Simulation (Top 2 Skills)
        cumulative_skills = []
        for roi in rois[:2]:
            cumulative_skills.append(roi.skill)
            state_name = f"After learning {roi.skill}"
            sim_state = self.impact_engine.simulate(candidate, cumulative_skills, state_name)
            simulations.append(sim_state)
            
        # 4. Analyze Synergy
        synergy = self.synergy_analyzer.analyze_combinations(candidate, base_state, rois, max_combo_size=2)
        
        # 5. Build Curriculum
        milestones = self.curriculum_gen.generate(rois)
        
        # 6. Evaluate
        total_hours = sum(m.estimated_hours for m in milestones)
        salary_gain = milestones[-1].expected_salary_delta if milestones else 0.0
        
        plan = LearningPlan(
            candidate_role=candidate.current_role or "Candidate",
            milestones=milestones,
            skill_rois=rois[:8],
            top_synergy=synergy,
            simulations=simulations,
            evaluation=None, # Will inject below
            total_estimated_hours=total_hours,
            projected_salary_gain_pct=round(salary_gain, 1)
        )
        
        plan.evaluation = self.evaluator.evaluate(plan)
        return plan

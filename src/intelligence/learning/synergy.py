from typing import List
from itertools import combinations
from src.intelligence.career.profiles.candidate import CandidateProfile
from src.intelligence.learning.impact import LearningImpactEngine
from src.intelligence.learning.models import SkillSynergy, SkillROI, SimulationState
from src.intelligence.learning.graph import LearningGraph

class SkillSynergyAnalyzer:
    def __init__(self, impact_engine: LearningImpactEngine, graph: LearningGraph):
        self.impact_engine = impact_engine
        self.graph = graph

    def analyze_combinations(self, candidate: CandidateProfile, base_state: SimulationState, top_skills: List[SkillROI], max_combo_size: int = 2) -> SkillSynergy:
        if not top_skills:
            return None
            
        skills_to_test = [r.skill for r in top_skills[:5]]
        best_synergy = None
        best_score = -1
        
        for size in range(2, max_combo_size + 1):
            for combo in combinations(skills_to_test, size):
                combo_list = list(combo)
                state = self.impact_engine.simulate(candidate, combo_list, "Synergy_Test")
                
                jobs_unlocked = max(0, state.career_paths - base_state.career_paths)
                salary_gain_pct = 0.0
                if base_state.average_salary > 0:
                    salary_gain_pct = ((state.average_salary - base_state.average_salary) / base_state.average_salary) * 100.0
                    
                total_hours = sum(self.graph.get_node(s).estimated_hours if self.graph.get_node(s) else 20.0 for s in combo_list)
                
                score = (state.match_confidence * jobs_unlocked * max(salary_gain_pct, 1.0)) / max(total_hours, 1.0)
                
                if score > best_score:
                    best_score = score
                    best_synergy = SkillSynergy(
                        skills=combo_list,
                        estimated_learning_time=total_hours,
                        jobs_unlocked=jobs_unlocked,
                        salary_increase_pct=round(salary_gain_pct, 1),
                        confidence=state.match_confidence
                    )
                    
        return best_synergy

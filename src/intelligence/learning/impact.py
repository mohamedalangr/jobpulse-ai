from typing import List
from src.intelligence.career.profiles.candidate import CandidateProfile
from src.intelligence.career.matching.matcher import SemanticMatcher
from src.intelligence.career.explainability.engine import ExplainabilityEngine
from src.intelligence.learning.models import ProjectedCandidateProfile, SimulationState
from src.intelligence.career.explainability.models import JobRecommendation

class LearningImpactEngine:
    def __init__(self, matcher: SemanticMatcher, explainer: ExplainabilityEngine):
        self.matcher = matcher
        self.explainer = explainer

    def simulate(self, base_profile: CandidateProfile, skills_to_add: List[str], state_name: str) -> SimulationState:
        projected_skills = list(dict.fromkeys(base_profile.skills + skills_to_add))
        
        projected = ProjectedCandidateProfile(
            base_profile=base_profile,
            simulated_skills=skills_to_add
        )
        
        temp_candidate = CandidateProfile(
            skills=projected_skills,
            experience=base_profile.experience,
            current_role=base_profile.current_role,
            years_experience=base_profile.years_experience,
            education=base_profile.education,
            desired_roles=base_profile.desired_roles,
            preferred_locations=base_profile.preferred_locations,
            salary_expectation=base_profile.salary_expectation,
            embedding=None
        )
        
        matches = self.matcher.find_nearest_jobs(temp_candidate, top_k=20)
        recs = self.explainer.explain(temp_candidate, matches)
        
        return self._build_state(state_name, skills_to_add, recs)

    def _build_state(self, name: str, added: List[str], recs: List[JobRecommendation]) -> SimulationState:
        if not recs:
            return SimulationState(name, added, 0.0, 0.0, 0.0, 0)
            
        avg_conf = sum(r.confidence for r in recs) / len(recs)
        avg_sim = sum(r.similarity_score for r in recs) / len(recs)
        
        valid_sals = [r.job.salary_max for r in recs if r.job.salary_max]
        avg_sal = sum(float(s) for s in valid_sals) / len(valid_sals) if valid_sals else 0.0
        
        titles = len(set(r.job.title for r in recs if r.job.title))
        
        return SimulationState(
            state_name=name,
            added_skills=added,
            match_confidence=round(avg_conf, 3),
            average_similarity=round(avg_sim, 3),
            average_salary=round(avg_sal, 0),
            career_paths=titles
        )

from dataclasses import dataclass, field
from typing import List, Optional
import numpy as np
from src.intelligence.career.profiles.candidate import CandidateProfile

@dataclass
class ProjectedCandidateProfile:
    base_profile: CandidateProfile
    simulated_skills: List[str]
    projected_embedding: Optional[np.ndarray] = None
    
    @property
    def all_skills(self) -> List[str]:
        # Return unique skills combining base and simulated
        return list(dict.fromkeys([s.lower() for s in self.base_profile.skills] + [s.lower() for s in self.simulated_skills]))

@dataclass
class SimulationState:
    state_name: str
    added_skills: List[str]
    match_confidence: float
    average_similarity: float
    average_salary: float
    career_paths: int

@dataclass
class SkillROI:
    skill: str
    learning_time_hours: float
    jobs_unlocked: int
    salary_gain_pct: float
    roi_score: float
    roi_rating: str # Excellent, Good, Fair

@dataclass
class SkillSynergy:
    skills: List[str]
    estimated_learning_time: float
    jobs_unlocked: int
    salary_increase_pct: float
    confidence: float

@dataclass
class LearningMilestone:
    title: str
    estimated_hours: float
    skills: List[str]
    unlocks: List[str]
    expected_salary_delta: float

@dataclass
class LearningPlanEvaluation:
    average_salary_gain: float
    average_similarity_gain: float
    average_jobs_unlocked: float
    average_learning_hours: float
    roi_score: float

@dataclass
class LearningPlan:
    candidate_role: str
    milestones: List[LearningMilestone]
    skill_rois: List[SkillROI]
    top_synergy: Optional[SkillSynergy]
    simulations: List[SimulationState]
    evaluation: LearningPlanEvaluation
    total_estimated_hours: float
    projected_salary_gain_pct: float

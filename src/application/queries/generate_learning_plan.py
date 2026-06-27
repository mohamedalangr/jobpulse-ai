from dataclasses import dataclass
from src.application.queries.base import QueryHandler
from src.application.context import RequestContext
from src.application.dto.internal.candidate import CandidateInputDTO
from src.intelligence.career.profiles.candidate import CandidateProfile
from src.intelligence.learning.models import LearningPlan

@dataclass
class GenerateLearningPlanQuery:
    candidate: CandidateInputDTO

class GenerateLearningPlanUseCase(QueryHandler):
    def __init__(self, semantic_matcher, explainability_engine, learning_planner):
        self.matcher = semantic_matcher
        self.explainer = explainability_engine
        self.planner = learning_planner

    def execute(self, query: GenerateLearningPlanQuery, context: RequestContext) -> LearningPlan:
        domain_candidate = CandidateProfile(
            skills=query.candidate.skills,
            experience=query.candidate.experience,
            current_role=query.candidate.current_role,
            years_experience=query.candidate.years_experience,
            education=query.candidate.education,
            desired_roles=query.candidate.desired_roles or [],
            preferred_locations=query.candidate.preferred_locations or [],
            salary_expectation=query.candidate.salary_expectation
        )
        
        matches = self.matcher.find_nearest_jobs(domain_candidate, top_k=20)
        recs = self.explainer.explain(domain_candidate, matches)
        
        plan = self.planner.generate_plan(domain_candidate, recs)
        return plan

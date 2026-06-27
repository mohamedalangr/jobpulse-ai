from dataclasses import dataclass
from src.application.queries.base import QueryHandler
from src.application.context import RequestContext
from src.application.dto.internal.candidate import CandidateInputDTO
from src.intelligence.career.profiles.candidate import CandidateProfile
from src.intelligence.career.matching.models import RecommendationResult

@dataclass
class AnalyzeCandidateQuery:
    candidate: CandidateInputDTO
    top_k: int = 15

class AnalyzeCandidateUseCase(QueryHandler):
    def __init__(self, semantic_matcher, explainability_engine, market_assessor, graph_gen, insights_engine, evaluator):
        self.matcher = semantic_matcher
        self.explainer = explainability_engine
        self.assessor = market_assessor
        self.graph_gen = graph_gen
        self.insights = insights_engine
        self.evaluator = evaluator

    def execute(self, query: AnalyzeCandidateQuery, context: RequestContext) -> RecommendationResult:
        # 1. Map DTO to Domain
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
        
        # 2. Execute Intelligence Workflow
        matches = self.matcher.find_nearest_jobs(domain_candidate, top_k=query.top_k)
        recommendations = self.explainer.explain(domain_candidate, matches)
        market_score = self.assessor.assess(domain_candidate, recommendations)
        transitions = self.graph_gen.generate(domain_candidate, recommendations)
        insights = self.insights.generate(recommendations, transitions)
        evaluation = self.evaluator.evaluate(recommendations, total_jobs_in_db=1000)
        
        return RecommendationResult(
            recommendations=recommendations,
            transition_path=transitions,
            insights=insights,
            evaluation=evaluation
        )

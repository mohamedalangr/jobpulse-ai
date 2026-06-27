from dataclasses import dataclass
from typing import List, Tuple
from src.application.queries.base import QueryHandler
from src.application.context import RequestContext
from src.domain.entities.job_posting import JobPosting

@dataclass
class SearchJobsQuery:
    query: str
    top_k: int = 10

class SearchJobsUseCase(QueryHandler):
    def __init__(self, semantic_matcher):
        self.matcher = semantic_matcher

    def execute(self, query: SearchJobsQuery, context: RequestContext) -> List[Tuple[JobPosting, float]]:
        # Future: return SearchResultItemDTOs
        return self.matcher.search(query.query, top_k=query.top_k)

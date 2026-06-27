import time
from dataclasses import dataclass
from typing import List, Tuple
from src.domain.entities.job_posting import JobPosting
from src.intelligence.semantic_search.service import SemanticSearchService

@dataclass
class SemanticSearchReport:
    query: str
    top_k: int
    latency_ms: float
    returned_results: int
    results: List[Tuple[JobPosting, float]]

class SemanticSearchEvaluator:
    def __init__(self, service: SemanticSearchService):
        self.service = service

    def evaluate(self, query: str, top_k: int = 5) -> SemanticSearchReport:
        start = time.perf_counter()
        results = self.service.search(query, top_k=top_k)
        duration_ms = (time.perf_counter() - start) * 1000
        
        return SemanticSearchReport(
            query=query,
            top_k=top_k,
            latency_ms=duration_ms,
            returned_results=len(results),
            results=results
        )

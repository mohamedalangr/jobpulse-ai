import numpy as np
from typing import List, Tuple
from src.domain.entities.job_posting import JobPosting
from src.intelligence.embeddings.base import EmbeddingProvider
from src.intelligence.vectorstore.base import VectorStore
from src.intelligence.semantic_search.service import JobFetcher
from src.intelligence.career.profiles.candidate import CandidateProfile

class CandidateEmbeddingBuilder:
    @staticmethod
    def build(candidate: CandidateProfile) -> str:
        parts = []
        if candidate.current_role:
            parts.append(f"Role: {candidate.current_role}")
        if candidate.experience:
            parts.append(f"Experience: {candidate.experience}")
        if candidate.skills:
            parts.append(f"Skills: {', '.join(candidate.skills)}")
        if candidate.education:
            parts.append(f"Education: {candidate.education}")
        return " | ".join(parts)

class SemanticMatcher:
    def __init__(self, provider: EmbeddingProvider, store: VectorStore, fetcher: JobFetcher):
        self.provider = provider
        self.store = store
        self.fetcher = fetcher

    def find_nearest_jobs(self, candidate: CandidateProfile, top_k: int = 15) -> List[Tuple[JobPosting, float]]:
        if candidate.embedding is None:
            text = CandidateEmbeddingBuilder.build(candidate)
            candidate.embedding = self.provider.embed(text)
            
        query_vector = candidate.embedding
        if len(query_vector.shape) == 1:
            query_vector = np.expand_dims(query_vector, axis=0)
            
        distances, ids_list = self.store.search(query_vector, top_k=top_k)
        
        matched_ids = ids_list[0]
        matched_distances = distances[0]
        
        results = []
        for fingerprint, dist in zip(matched_ids, matched_distances):
            job = self.fetcher.get_by_fingerprint(fingerprint)
            if job:
                similarity = 1.0 / (1.0 + float(dist))
                results.append((job, similarity))
                
        results.sort(key=lambda x: x[1], reverse=True)
        return results

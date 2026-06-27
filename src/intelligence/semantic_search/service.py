from typing import List, Tuple, Protocol
import numpy as np
from src.domain.entities.job_posting import JobPosting
from src.intelligence.embeddings.base import EmbeddingProvider
from src.intelligence.vectorstore.base import VectorStore

class JobFetcher(Protocol):
    def get_by_fingerprint(self, fingerprint: str) -> JobPosting:
        ...

class SemanticSearchService:
    def __init__(self, provider: EmbeddingProvider, store: VectorStore, fetcher: JobFetcher):
        self.provider = provider
        self.store = store
        self.fetcher = fetcher

    def search(self, query: str, top_k: int = 5) -> List[Tuple[JobPosting, float]]:
        # 1. Embed query
        query_vector = self.provider.embed(query)
        if len(query_vector.shape) == 1:
            query_vector = np.expand_dims(query_vector, axis=0)
            
        # 2. Search FAISS
        distances, ids_list = self.store.search(query_vector, top_k=top_k)
        
        # 3. Retrieve objects
        matched_ids = ids_list[0]
        matched_distances = distances[0]
        
        results = []
        for fingerprint, dist in zip(matched_ids, matched_distances):
            job = self.fetcher.get_by_fingerprint(fingerprint)
            if job:
                # Convert L2 distance to a simple similarity bounded between 0 and 1
                similarity = 1.0 / (1.0 + float(dist))
                results.append((job, similarity))
                
        # Sort by similarity descending
        results.sort(key=lambda x: x[1], reverse=True)
        return results

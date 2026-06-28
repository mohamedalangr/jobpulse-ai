from typing import List, Tuple
import numpy as np
from sqlalchemy import select, func

from src.intelligence.vectorstore.base import VectorStore
from src.database.models.job import Job
from src.database.session import SessionLocal

class PgVectorStore(VectorStore):
    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def add(self, vectors: np.ndarray, ids: List[str]) -> None:
        """
        In the JobPulse architecture, vectors are generated and updated via the 
        Job entity. This method is provided for interface compatibility, but 
        actual upserts are handled through the JobRepository.
        """
        raise NotImplementedError("Use JobRepository to update embeddings in Supabase.")

    def search(self, query_vector: np.ndarray, top_k: int = 5) -> Tuple[np.ndarray, List[List[str]]]:
        """
        Searches for the closest vectors in pgvector.
        Returns: (distances, ids)
        """
        with self.session_factory() as session:
            # We use L2 distance (<->) here. 
            # Note: We return ids as strings wrapped in a list to match the FAISS return signature
            # which returns batched results: List[List[str]]
            
            # Ensure query_vector is 1D for pgvector
            if len(query_vector.shape) > 1:
                query_vector = query_vector.flatten()
                
            stmt = select(Job.fingerprint, Job.embedding.l2_distance(query_vector.tolist()).label("distance")) \
                .where(Job.embedding.is_not(None)) \
                .order_by("distance") \
                .limit(top_k)
                
            results = session.execute(stmt).all()
            
            distances = []
            ids = []
            
            for row in results:
                distances.append(row.distance)
                ids.append(str(row.fingerprint))
                
            # FAISS interface expects batches, e.g. [[id1, id2, ...]]
            return np.array([distances]), [ids]

    def save(self, filepath: str) -> None:
        pass # No-op for pgvector

    def load(self, filepath: str) -> None:
        pass # No-op for pgvector
        
    def count(self) -> int:
        with self.session_factory() as session:
            return session.scalar(select(func.count(Job.id)).where(Job.embedding.is_not(None)))

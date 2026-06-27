from abc import ABC, abstractmethod
from typing import List, Tuple
import numpy as np

class VectorStore(ABC):
    @abstractmethod
    def add(self, vectors: np.ndarray, ids: List[str]) -> None:
        pass

    @abstractmethod
    def search(self, query_vector: np.ndarray, top_k: int = 5) -> Tuple[np.ndarray, List[List[str]]]:
        """Returns (distances, ids)"""
        pass

    @abstractmethod
    def save(self, filepath: str) -> None:
        pass

    @abstractmethod
    def load(self, filepath: str) -> None:
        pass
        
    @abstractmethod
    def count(self) -> int:
        pass

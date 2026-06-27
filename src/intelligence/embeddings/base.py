from abc import ABC, abstractmethod
from typing import List
import numpy as np

class EmbeddingProvider(ABC):
    @abstractmethod
    def embed(self, text: str) -> np.ndarray:
        """Encode a single string into a semantic embedding vector."""
        pass

    @abstractmethod
    def embed_many(self, texts: List[str]) -> np.ndarray:
        """Encode a list of strings into a matrix of embedding vectors."""
        pass

from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from src.intelligence.embeddings.base import EmbeddingProvider

class SentenceTransformerProvider(EmbeddingProvider):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = SentenceTransformer(model_name)

    def embed(self, text: str) -> np.ndarray:
        return self._model.encode(text, convert_to_numpy=True)

    def embed_many(self, texts: List[str]) -> np.ndarray:
        return self._model.encode(texts, convert_to_numpy=True)

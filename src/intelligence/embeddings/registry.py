from typing import Dict, Type, Any
from src.intelligence.embeddings.base import EmbeddingProvider
from src.intelligence.embeddings.providers.sentence_transformer import SentenceTransformerProvider

class EmbeddingRegistry:
    def __init__(self):
        self._providers: Dict[str, Type[EmbeddingProvider]] = {
            "sentence_transformer": SentenceTransformerProvider
        }
        
    def register(self, name: str, provider_cls: Type[EmbeddingProvider]) -> None:
        self._providers[name] = provider_cls

    def get_provider(self, name: str, **kwargs: Any) -> EmbeddingProvider:
        if name not in self._providers:
            raise ValueError(f"Unknown embedding provider: {name}")
        return self._providers[name](**kwargs)

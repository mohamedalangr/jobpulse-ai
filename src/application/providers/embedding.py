from typing import Any, Dict
from src.application.providers.base import Provider
from src.application.providers.runtime import get_runtime_registry
from src.application.models.registry import ModelRegistry
from src.intelligence.embeddings.registry import EmbeddingRegistry as InternalEmbeddingRegistry

class EmbeddingProvider(Provider):
    """Lazy-loads the embedding model on first use."""
    def __init__(self, model_registry: ModelRegistry, model_key: str = "default_embedding"):
        self.model_registry = model_registry
        self.model_key = model_key
        self.descriptor = self.model_registry.get_embedding(self.model_key)
        
        self._provider = None

    def _ensure_loaded(self):
        if self._provider is None:
            registry = InternalEmbeddingRegistry()
            provider_type = self.descriptor.provider if self.descriptor.provider != "sentence_transformer" else "hosted_openai"
            self._provider = registry.get_provider(provider_type, model_name=self.descriptor.id)
            get_runtime_registry().register(f"embedding_{self.model_key}", self._provider)

    def embed(self, text: str) -> Any:
        self._ensure_loaded()
        return self._provider.embed(text)

    def health(self) -> Dict[str, Any]:
        return {
            "status": "up" if self._provider else "uninitialized",
            "model": self.descriptor.id,
            "dimension": self.descriptor.dimension
        }

    def close(self) -> None:
        self._provider = None
        
def get_embedding_provider(model_registry: ModelRegistry) -> EmbeddingProvider:
    return EmbeddingProvider(model_registry)

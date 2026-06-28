from typing import Any, Dict
from src.application.providers.base import Provider
from src.application.providers.runtime import get_runtime_registry
from src.application.models.registry import ModelRegistry
from src.intelligence.embeddings.registry import EmbeddingRegistry as InternalEmbeddingRegistry
import os

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
            provider_type = self.descriptor.provider
            if "sentence" in provider_type or provider_type not in ["hosted_openai", "hosted_huggingface", "hosted_gemini"]:
                provider_type = os.environ.get("EMBEDDING_PROVIDER", "hosted_gemini")
                
            # If we fallback to a cloud provider, use their default model instead of the local one
            if provider_type == "hosted_gemini":
                model_name = "gemini-embedding-2"
            elif provider_type == "hosted_openai":
                model_name = "text-embedding-3-small"
            else:
                model_name = self.descriptor.id
                
            self._provider = registry.get_provider(provider_type, model_name=model_name)
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

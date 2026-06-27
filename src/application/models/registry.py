from typing import Dict, Optional
from src.application.models.descriptor import ModelDescriptor
from src.application.models.types import ModelCategory
from src.application.config.settings import ConfigManager

class ModelRegistry:
    """Static registry of available models populated via YAML configuration."""
    def __init__(self, config_manager: ConfigManager):
        self.models: Dict[str, ModelDescriptor] = {}
        self._load_from_config(config_manager)

    def _load_from_config(self, config_manager: ConfigManager):
        settings = config_manager.model_settings.models
        for key, conf in settings.items():
            descriptor = ModelDescriptor(
                id=conf.id,
                name=conf.name,
                version=conf.version,
                category=ModelCategory(conf.category),
                provider=conf.provider,
                dimension=conf.dimension,
                framework=conf.framework,
                checksum=conf.checksum
            )
            self.models[key] = descriptor

    def get_model(self, key: str) -> Optional[ModelDescriptor]:
        return self.models.get(key)
        
    def get_embedding(self, key: str = "default_embedding") -> ModelDescriptor:
        model = self.get_model(key)
        if not model or model.category != ModelCategory.EMBEDDING:
            raise ValueError(f"Invalid or missing embedding model: {key}")
        return model

    def get_clusterer(self, key: str = "default_clusterer") -> ModelDescriptor:
        model = self.get_model(key)
        if not model or model.category != ModelCategory.CLUSTERER:
            raise ValueError(f"Invalid or missing clusterer model: {key}")
        return model

    def get_reducer(self, key: str = "default_reducer") -> ModelDescriptor:
        model = self.get_model(key)
        if not model or model.category != ModelCategory.REDUCER:
            raise ValueError(f"Invalid or missing reducer model: {key}")
        return model

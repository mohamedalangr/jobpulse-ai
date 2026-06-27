import yaml
from typing import Dict, Any, Type, TypeVar
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class EmbeddingConfig(BaseModel):
    provider: str
    model: str
    batch_size: int = 64
    normalize: bool = True

class VectorStoreConfig(BaseModel):
    backend: str
    dimension: int
    top_k: int = 5

class SemanticSearchConfig(BaseModel):
    embedding: EmbeddingConfig
    vector_store: VectorStoreConfig

class SkillOntologyConfig(BaseModel):
    ontology_path: str = "config/skills.yaml"

class ExperimentConfig(BaseModel):
    experiment_id: str
    description: str
    semantic_search: SemanticSearchConfig

class ConfigLoader:
    @staticmethod
    def load_yaml(filepath: str) -> Dict[str, Any]:
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}

    @staticmethod
    def load(filepath: str, model_class: Type[T]) -> T:
        data = ConfigLoader.load_yaml(filepath)
        return model_class.model_validate(data)

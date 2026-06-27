from dataclasses import dataclass
from typing import Optional, Dict, Any
from src.application.models.types import ModelCategory

@dataclass(frozen=True)
class ModelDescriptor:
    id: str
    name: str
    version: str
    category: ModelCategory
    provider: str
    dimension: Optional[int]
    framework: str
    checksum: Optional[str]
    config: Dict[str, Any] = None
    metadata: Dict[str, Any] = None

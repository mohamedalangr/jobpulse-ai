from dataclasses import dataclass, field
from typing import List, Dict, Any
import numpy as np

@dataclass
class EmbeddingDataset:
    embeddings: np.ndarray
    fingerprints: List[str]
    model_name: str
    metadata: Dict[str, Any] = field(default_factory=dict)

from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class ClusteringConfig:
    algorithm_name: str
    random_seed: int
    parameters: Dict[str, Any] = field(default_factory=dict)

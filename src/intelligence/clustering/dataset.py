from dataclasses import dataclass
from typing import Optional
import numpy as np
from src.intelligence.analytics.dataset import EmbeddingDataset
from src.intelligence.clustering.config import ClusteringConfig

@dataclass
class ClusterDataset:
    base_dataset: EmbeddingDataset
    config: ClusteringConfig
    assignments: np.ndarray # Array of cluster IDs (-1 for noise)
    reduced_coordinates: Optional[np.ndarray] = None # Optional 2D representation for visualization

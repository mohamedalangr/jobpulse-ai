import numpy as np
from src.intelligence.analytics.dataset import EmbeddingDataset
from src.intelligence.clustering.base import ClusterAlgorithm

class HDBSCANClusterer(ClusterAlgorithm):
    def __init__(self, min_cluster_size: int = 5, min_samples: int = None):
        self.min_cluster_size = min_cluster_size
        self.min_samples = min_samples

    def fit_predict(self, dataset: EmbeddingDataset) -> np.ndarray:
        try:
            from sklearn.cluster import HDBSCAN
        except ImportError:
            raise ImportError("HDBSCAN requires scikit-learn>=1.3.0")

        hdbscan = HDBSCAN(min_cluster_size=self.min_cluster_size, min_samples=self.min_samples)
        return hdbscan.fit_predict(dataset.embeddings)

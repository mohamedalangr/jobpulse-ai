import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
import numpy as np
from src.intelligence.analytics.dataset import EmbeddingDataset

class Reducer(ABC):
    @abstractmethod
    def reduce(self, dataset: EmbeddingDataset) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Reduces dimensionality.
        Returns:
            - np.ndarray: The 2D reduced vectors.
            - Dict: Metrics/Evaluation details (e.g. execution_time_ms).
        """
        pass

class PCAReducer(Reducer):
    def __init__(self, n_components: int = 2):
        self.n_components = n_components

    def reduce(self, dataset: EmbeddingDataset) -> Tuple[np.ndarray, Dict[str, Any]]:
        from sklearn.decomposition import PCA
        
        start = time.perf_counter()
        pca = PCA(n_components=self.n_components, random_state=42)
        reduced = pca.fit_transform(dataset.embeddings)
        duration_ms = (time.perf_counter() - start) * 1000
        
        variance = float(np.sum(pca.explained_variance_ratio_))
        
        metrics = {
            "reducer": "PCA",
            "execution_time_ms": duration_ms,
            "input_dimension": dataset.embeddings.shape[1],
            "output_dimension": self.n_components,
            "samples": dataset.embeddings.shape[0],
            "explained_variance": variance
        }
        return reduced, metrics

class UMAPReducer(Reducer):
    def __init__(self, n_neighbors: int = 15, min_dist: float = 0.1, metric: str = 'cosine'):
        self.n_neighbors = n_neighbors
        self.min_dist = min_dist
        self.metric = metric

    def reduce(self, dataset: EmbeddingDataset) -> Tuple[np.ndarray, Dict[str, Any]]:
        import umap
        
        start = time.perf_counter()
        reducer = umap.UMAP(
            n_neighbors=self.n_neighbors,
            min_dist=self.min_dist,
            metric=self.metric,
            n_components=2,
            random_state=42 # Deterministic for reproducibility
        )
        reduced = reducer.fit_transform(dataset.embeddings)
        duration_ms = (time.perf_counter() - start) * 1000
        
        metrics = {
            "reducer": "UMAP",
            "execution_time_ms": duration_ms,
            "input_dimension": dataset.embeddings.shape[1],
            "output_dimension": 2,
            "samples": dataset.embeddings.shape[0],
            "n_neighbors": self.n_neighbors,
            "min_dist": self.min_dist,
            "metric": self.metric
        }
        return reduced, metrics
        
class TSNEReducer(Reducer):
    """Stub for future TSNE implementation"""
    def reduce(self, dataset: EmbeddingDataset) -> Tuple[np.ndarray, Dict[str, Any]]:
        raise NotImplementedError("t-SNE reducer not yet implemented")

import numpy as np
from src.intelligence.analytics.dataset import EmbeddingDataset
from src.intelligence.clustering.base import ClusterAlgorithm
from sklearn.cluster import AgglomerativeClustering

class AgglomerativeClusterer(ClusterAlgorithm):
    def __init__(self, n_clusters: int = 8):
        self.n_clusters = n_clusters

    def fit_predict(self, dataset: EmbeddingDataset) -> np.ndarray:
        agg = AgglomerativeClustering(n_clusters=self.n_clusters)
        return agg.fit_predict(dataset.embeddings)

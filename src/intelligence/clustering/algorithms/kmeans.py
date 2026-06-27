import numpy as np
from src.intelligence.analytics.dataset import EmbeddingDataset
from src.intelligence.clustering.base import ClusterAlgorithm
from sklearn.cluster import KMeans

class KMeansClusterer(ClusterAlgorithm):
    def __init__(self, n_clusters: int = 8, random_state: int = 42):
        self.n_clusters = n_clusters
        self.random_state = random_state

    def fit_predict(self, dataset: EmbeddingDataset) -> np.ndarray:
        kmeans = KMeans(n_clusters=self.n_clusters, random_state=self.random_state, n_init='auto')
        return kmeans.fit_predict(dataset.embeddings)

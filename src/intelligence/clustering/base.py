from abc import ABC, abstractmethod
import numpy as np
from src.intelligence.analytics.dataset import EmbeddingDataset

class ClusterAlgorithm(ABC):
    @abstractmethod
    def fit_predict(self, dataset: EmbeddingDataset) -> np.ndarray:
        """
        Returns an array of cluster assignments corresponding to the dataset's embeddings.
        Outliers/noise should be denoted as -1.
        """
        pass

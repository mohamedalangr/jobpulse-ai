from dataclasses import dataclass
import numpy as np
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from src.intelligence.clustering.dataset import ClusterDataset

@dataclass
class ClusterEvaluation:
    silhouette_score: float
    davies_bouldin: float
    calinski_harabasz: float
    noise_ratio: float
    cluster_count: int
    average_cluster_size: float

class ClusterEvaluator:
    def evaluate(self, dataset: ClusterDataset) -> ClusterEvaluation:
        labels = dataset.assignments
        embeddings = dataset.base_dataset.embeddings
        
        valid_idx = labels != -1
        valid_labels = labels[valid_idx]
        valid_embeddings = embeddings[valid_idx]
        
        cluster_count = len(set(valid_labels))
        
        if cluster_count > 1 and len(valid_labels) > cluster_count:
            sil = float(silhouette_score(valid_embeddings, valid_labels))
            db = float(davies_bouldin_score(valid_embeddings, valid_labels))
            ch = float(calinski_harabasz_score(valid_embeddings, valid_labels))
        else:
            sil, db, ch = 0.0, 0.0, 0.0
            
        noise_ratio = float(np.sum(labels == -1) / len(labels)) if len(labels) > 0 else 0.0
        avg_size = float(len(valid_labels) / cluster_count) if cluster_count > 0 else 0.0
        
        return ClusterEvaluation(
            silhouette_score=sil,
            davies_bouldin=db,
            calinski_harabasz=ch,
            noise_ratio=noise_ratio,
            cluster_count=cluster_count,
            average_cluster_size=avg_size
        )

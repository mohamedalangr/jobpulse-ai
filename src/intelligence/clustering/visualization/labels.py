from typing import List, Dict
from src.intelligence.analytics.labels import LabelProvider
from src.intelligence.semantic_search.service import JobFetcher
from src.intelligence.clustering.labeling import ClusterLabel
from src.intelligence.clustering.dataset import ClusterDataset

class ClusterLabelProvider(LabelProvider):
    def __init__(self, dataset: ClusterDataset, labels: Dict[int, ClusterLabel]):
        self.dataset = dataset
        self.labels = labels

    def get_labels(self, fingerprints: List[str], fetcher: JobFetcher) -> List[str]:
        fp_to_idx = {fp: i for i, fp in enumerate(self.dataset.base_dataset.fingerprints)}
        
        results = []
        for fp in fingerprints:
            idx = fp_to_idx.get(fp)
            if idx is not None:
                cluster_id = self.dataset.assignments[idx]
                if cluster_id == -1:
                    results.append("Outlier/Noise")
                else:
                    cl = self.labels.get(cluster_id)
                    results.append(cl.label if cl else f"Cluster {cluster_id}")
            else:
                results.append("Unknown")
        return results

import numpy as np
from src.intelligence.analytics.dataset import EmbeddingDataset
from src.intelligence.clustering.config import ClusteringConfig
from src.intelligence.clustering.dataset import ClusterDataset
from src.intelligence.clustering.algorithms.kmeans import KMeansClusterer
from src.intelligence.clustering.labeling import FrequencyClusterLabeler
from src.intelligence.clustering.summaries import ClusterSummary

def test_kmeans_clusterer():
    embeddings = np.random.rand(20, 384)
    dataset = EmbeddingDataset(embeddings=embeddings, fingerprints=[f"fp_{i}" for i in range(20)], model_name="test")
    clusterer = KMeansClusterer(n_clusters=2)
    assignments = clusterer.fit_predict(dataset)
    
    assert len(assignments) == 20
    assert set(assignments).issubset({0, 1})

def test_frequency_labeler():
    summary = ClusterSummary(
        cluster_id=0,
        size=10,
        median_salary=100000.0,
        top_companies=["A"],
        top_skills=["python", "docker"],
        top_titles=["Software Engineer", "Backend Developer"],
        remote_ratio=0.5,
        representative_jobs=[]
    )
    labeler = FrequencyClusterLabeler()
    label = labeler.generate_label(summary)
    
    assert label.cluster_id == 0
    assert label.label == "Software Engineer"

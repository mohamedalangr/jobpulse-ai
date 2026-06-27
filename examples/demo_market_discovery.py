import os
import json
import numpy as np
from src.ingestion.manager import IngestionManager
from src.ingestion.scrapers.remoteok import RemoteOKScraper
from src.ingestion.registry import SourceRegistry
from src.processing.pipeline import ProcessingPipeline
from src.processing.stages.validation import ValidationStage
from src.processing.stages.cleaning import CleaningStage
from src.processing.stages.normalization import NormalizationStage
from src.processing.stages.fingerprint import FingerprintStage
from src.processing.stages.deduplication import DeduplicationStage
from src.processing.deduplication.memory_store import MemoryDuplicateStore
from src.processing.deduplication.detector import DuplicateDetector

from src.intelligence.embeddings.registry import EmbeddingRegistry
from src.intelligence.embeddings.cache import EmbeddingCache
from src.intelligence.text_builder import TextBuilder

from src.intelligence.analytics.dataset import EmbeddingDataset
from src.intelligence.analytics.reducers import UMAPReducer
from src.intelligence.analytics.visualizer import MatplotlibVisualizer
from src.intelligence.semantic_search.service import JobFetcher
from src.domain.entities.job_posting import JobPosting
from typing import List

from src.intelligence.clustering.config import ClusteringConfig
from src.intelligence.clustering.dataset import ClusterDataset
from src.intelligence.clustering.algorithms.hdbscan import HDBSCANClusterer
from src.intelligence.clustering.analyzers.analyzer import ClusterAnalyzer
from src.intelligence.clustering.labeling import FrequencyClusterLabeler
from src.intelligence.clustering.renderers.markdown import MarketReportGenerator
from src.intelligence.clustering.evaluation import ClusterEvaluator
from src.intelligence.clustering.visualization.labels import ClusterLabelProvider

class InMemoryFetcher(JobFetcher):
    def __init__(self, jobs: List[JobPosting]):
        self.jobs_by_fp = {j.metadata.fingerprint: j for j in jobs if j.metadata and j.metadata.fingerprint}
        
    def get_by_fingerprint(self, fingerprint: str) -> JobPosting:
        return self.jobs_by_fp.get(fingerprint)

def main():
    print("========================================")
    print("JobPulse AI")
    print("Semantic Market Discovery")
    print("========================================")
    print("\nLoading embeddings...")
    
    registry = SourceRegistry()
    registry.register(RemoteOKScraper())
    manager = IngestionManager(registry)
    jobs, _ = manager.run_all()
    
    detector = DuplicateDetector(MemoryDuplicateStore())
    pipeline = ProcessingPipeline([
        ValidationStage(),
        CleaningStage(),
        NormalizationStage(),
        FingerprintStage(),
        DeduplicationStage(detector)
    ])
    processed_jobs, _ = pipeline.process(jobs)
    
    embed_registry = EmbeddingRegistry()
    model_name = "all-MiniLM-L6-v2"
    provider = embed_registry.get_provider("sentence_transformer", model_name=model_name)
    cache = EmbeddingCache(model_name=model_name, base_dir="artifacts/embeddings")
    
    vectors, fps = [], []
    for job in processed_jobs:
        fp = job.metadata.fingerprint
        if not fp: continue
        vector = cache.get(fp)
        if vector is None:
            text = TextBuilder.build(job)
            vector = provider.embed(text)
            cache.add(fp, vector)
        vectors.append(vector)
        fps.append(fp)
        
    cache.save()
    
    dataset = EmbeddingDataset(
        embeddings=np.vstack(vectors),
        fingerprints=fps,
        model_name=model_name,
        metadata={"dataset_version": "v1.0"}
    )
    
    print(f"{len(fps)} vectors loaded")
    
    print("\nRunning UMAP...")
    reducer = UMAPReducer(n_neighbors=15, min_dist=0.1)
    reduced_vectors, red_metrics = reducer.reduce(dataset)
    
    print("\nRunning HDBSCAN...")
    hdbscan_config = ClusteringConfig(algorithm_name="HDBSCAN", random_seed=42, parameters={"min_cluster_size": 5})
    hdbscan = HDBSCANClusterer(min_cluster_size=5)
    assignments = hdbscan.fit_predict(dataset)
    
    cluster_dataset = ClusterDataset(
        base_dataset=dataset,
        config=hdbscan_config,
        assignments=assignments,
        reduced_coordinates=reduced_vectors
    )
    
    print("Generating summaries...")
    fetcher = InMemoryFetcher(processed_jobs)
    analyzer = ClusterAnalyzer(fetcher)
    report = analyzer.analyze(cluster_dataset)
    
    print(f"{len(report.summaries)} clusters discovered")
    
    print("Generating labels...")
    labeler = FrequencyClusterLabeler()
    cluster_labels = {}
    for summary in report.summaries:
        cluster_labels[summary.cluster_id] = labeler.generate_label(summary)
        
    print("Evaluating quality...")
    evaluator = ClusterEvaluator()
    evaluation = evaluator.evaluate(cluster_dataset)
    
    print(f"Average Silhouette Score: {evaluation.silhouette_score:.2f}")
    
    print("\nTop Clusters")
    for i, summary in enumerate(report.summaries[:3]):
        label = cluster_labels[summary.cluster_id].label
        print(f"\n{i+1}.\n{label}\nJobs: {summary.size}\nTop Skills:")
        for skill in summary.top_skills[:3]:
            print(f"- {skill}")
            
    print("\nSaving report...")
    report_gen = MarketReportGenerator()
    report_path = "artifacts/market_discovery/reports/market_report.md"
    report_gen.render(report, cluster_labels, report_path)
    
    print("Saving metrics...")
    os.makedirs("artifacts/market_discovery/metrics", exist_ok=True)
    with open("artifacts/market_discovery/metrics/cluster_metrics.json", "w") as f:
        json.dump(evaluation.__dict__, f, indent=2)
        
    print("Saving visualization...")
    viz_dir = "artifacts/market_discovery/visualizations"
    label_provider = ClusterLabelProvider(cluster_dataset, cluster_labels)
    viz_labels = label_provider.get_labels(dataset.fingerprints, fetcher)
    MatplotlibVisualizer().render(dataset, reduced_vectors, viz_labels, red_metrics, viz_dir)
    
    print("\nDone.")
    print("Artifacts generated in artifacts/market_discovery/")
    print("========================================")

if __name__ == "__main__":
    main()

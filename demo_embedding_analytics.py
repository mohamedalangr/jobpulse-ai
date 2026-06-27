import os
import sys
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
from src.intelligence.analytics.reducers import PCAReducer, UMAPReducer
from src.intelligence.analytics.labels import RemoteLabelProvider
from src.intelligence.analytics.visualizer import MatplotlibVisualizer
from src.intelligence.semantic_search.service import JobFetcher
from src.domain.entities.job_posting import JobPosting
from typing import List

class InMemoryFetcher(JobFetcher):
    def __init__(self, jobs: List[JobPosting]):
        self.jobs_by_fp = {j.metadata.fingerprint: j for j in jobs if j.metadata and j.metadata.fingerprint}
        
    def get_by_fingerprint(self, fingerprint: str) -> JobPosting:
        return self.jobs_by_fp.get(fingerprint)

def main():
    print("=" * 41)
    print("Embedding Analytics")
    print("=" * 41)
    
    # 1. Gather Job Postings
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
    
    # 2. Bootstrapping Embeddings
    print("\nLoading embeddings...")
    embed_registry = EmbeddingRegistry()
    model_name = "all-MiniLM-L6-v2"
    provider = embed_registry.get_provider("sentence_transformer", model_name=model_name)
    
    cache = EmbeddingCache(model_name=model_name, base_dir="artifacts/embeddings")
    
    vectors_to_add = []
    ids_to_add = []
    
    for job in processed_jobs:
        fp = job.metadata.fingerprint
        if not fp: continue
        
        vector = cache.get(fp)
        if vector is None:
            text = TextBuilder.build(job)
            vector = provider.embed(text)
            cache.add(fp, vector)
            
        vectors_to_add.append(vector)
        ids_to_add.append(fp)
        
    cache.save()
    
    # 3. Create Dataset
    dataset = EmbeddingDataset(
        embeddings=np.vstack(vectors_to_add),
        fingerprints=ids_to_add,
        model_name=model_name,
        metadata={"dataset_version": "v1.0"}
    )
    
    # 4. Analytics Setup
    fetcher = InMemoryFetcher(processed_jobs)
    label_provider = RemoteLabelProvider()
    labels = label_provider.get_labels(dataset.fingerprints, fetcher)
    
    visualizer = MatplotlibVisualizer()
    
    # 5. Run Reducers
    reducers = {
        "pca": PCAReducer(n_components=2),
        "umap": UMAPReducer(n_neighbors=15, min_dist=0.1)
    }
    
    for name, reducer in reducers.items():
        print(f"\nReducer: {name.upper()}")
        print("Rendering...")
        
        reduced_vectors, metrics = reducer.reduce(dataset)
        
        output_dir = os.path.join("artifacts", "visualization", name)
        png_path = visualizer.render(dataset, reduced_vectors, labels, metrics, output_dir)
        
        print(f"Saved:\n{png_path}")

    print("\nAnalytics Complete")

if __name__ == "__main__":
    main()

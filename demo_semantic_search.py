import os
import sys
from typing import List
from src.domain.entities.job_posting import JobPosting
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
from src.intelligence.vectorstore.faiss_store import FaissVectorStore
from src.intelligence.semantic_search.service import SemanticSearchService, JobFetcher
from src.intelligence.evaluation.semantic import SemanticSearchEvaluator

class InMemoryFetcher(JobFetcher):
    def __init__(self, jobs: List[JobPosting]):
        self.jobs_by_fp = {j.metadata.fingerprint: j for j in jobs if j.metadata and j.metadata.fingerprint}
        
    def get_by_fingerprint(self, fingerprint: str) -> JobPosting:
        return self.jobs_by_fp.get(fingerprint)

def main():
    print("=" * 41)
    print("JobPulse AI Semantic Search Demo")
    print("=" * 41)
    
    # 1. Ingestion
    print("\n[1] Ingesting jobs from RemoteOK...")
    registry = SourceRegistry()
    registry.register(RemoteOKScraper())
    manager = IngestionManager(registry)
    jobs, _ = manager.run_all()
    
    # 2. Processing
    print("[2] Processing jobs...")
    detector = DuplicateDetector(MemoryDuplicateStore())
    pipeline = ProcessingPipeline([
        ValidationStage(),
        CleaningStage(),
        NormalizationStage(),
        FingerprintStage(),
        DeduplicationStage(detector)
    ])
    processed_jobs, _ = pipeline.process(jobs)
    
    # 3. Setup Intelligence Layer
    print("[3] Bootstrapping Intelligence Layer...")
    
    embed_registry = EmbeddingRegistry()
    provider = embed_registry.get_provider("sentence_transformer", model_name="all-MiniLM-L6-v2")
    
    cache = EmbeddingCache(model_name="all-MiniLM-L6-v2", base_dir="artifacts/embeddings")
    
    # Generate/Retrieve Embeddings
    print(f"[4] Generating/Retrieving Embeddings for {len(processed_jobs)} jobs...")
    
    vectors_to_add = []
    ids_to_add = []
    
    # MiniLM dimension
    dim = 384
    store = FaissVectorStore(dimension=dim)
    
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
    
    # Add to FAISS
    import numpy as np
    if vectors_to_add:
        store.add(np.vstack(vectors_to_add), ids_to_add)
        
    # Semantic Search Service
    fetcher = InMemoryFetcher(processed_jobs)
    service = SemanticSearchService(provider=provider, store=store, fetcher=fetcher)
    evaluator = SemanticSearchEvaluator(service)
    
    # Run queries
    queries = [
        "Python backend engineer with Docker and AWS experience",
        "Frontend React developer for building user interfaces"
    ]
    
    for query in queries:
        print("\n=========================================")
        print(f"Query:\n\"{query}\"")
        
        report = evaluator.evaluate(query, top_k=3)
        print(f"\n[Latency: {report.latency_ms:.2f} ms]")
        print("\nTop Matches")
        
        for idx, (job, score) in enumerate(report.results, 1):
            print(f"\n{idx}.")
            print(f"{job.title}")
            print(f"{job.company}")
            print(f"\nSimilarity: {score:.2f}")
            print("-" * 25)

if __name__ == "__main__":
    main()

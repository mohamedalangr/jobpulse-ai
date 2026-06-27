import os
import numpy as np
import pytest
from src.intelligence.analytics.dataset import EmbeddingDataset
from src.intelligence.analytics.reducers import PCAReducer
from src.intelligence.analytics.labels import CompanyLabelProvider
from src.domain.entities.job_posting import JobPosting
from src.intelligence.semantic_search.service import JobFetcher

class MockJobFetcher(JobFetcher):
    def __init__(self, jobs):
        self.jobs = {j.metadata.fingerprint: j for j in jobs}
    def get_by_fingerprint(self, fingerprint: str) -> JobPosting:
        return self.jobs.get(fingerprint)

def test_pca_reducer():
    embeddings = np.random.rand(10, 384)
    fingerprints = [f"fp_{i}" for i in range(10)]
    dataset = EmbeddingDataset(
        embeddings=embeddings,
        fingerprints=fingerprints,
        model_name="test_model",
        metadata={"version": "1.0"}
    )
    
    reducer = PCAReducer(n_components=2)
    reduced, metrics = reducer.reduce(dataset)
    
    assert reduced.shape == (10, 2)
    assert metrics["reducer"] == "PCA"
    assert "explained_variance" in metrics
    assert metrics["samples"] == 10

def test_label_provider():
    from src.domain.entities.metadata import RecordMetadata
    from datetime import datetime, timezone
    
    job = JobPosting(
        id="1",
        title="Title",
        company="Amazon",
        description="Desc",
        url="http://test.com",
        raw_data={},
        metadata=RecordMetadata(
            fingerprint="fp_1", 
            source="test", 
            pipeline_version="1", 
            first_seen_at=datetime.now(timezone.utc), 
            last_seen_at=datetime.now(timezone.utc)
        )
    )
    fetcher = MockJobFetcher([job])
    provider = CompanyLabelProvider()
    
    labels = provider.get_labels(["fp_1", "fp_2"], fetcher)
    assert labels[0] == "Amazon"
    assert labels[1] == "Unknown"

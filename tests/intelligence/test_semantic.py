import os
import numpy as np
import pytest
from src.intelligence.embeddings.base import EmbeddingProvider
from src.intelligence.text_builder import TextBuilder
from src.intelligence.embeddings.cache import EmbeddingCache
from src.intelligence.vectorstore.faiss_store import FaissVectorStore
from src.intelligence.semantic_search.service import SemanticSearchService, JobFetcher
from src.domain.entities.job_posting import JobPosting
from src.domain.entities.metadata import RecordMetadata

class MockEmbeddingProvider(EmbeddingProvider):
    def embed(self, text: str) -> np.ndarray:
        return np.ones(384) * (len(text) / 100.0)

    def embed_many(self, texts: list[str]) -> np.ndarray:
        return np.array([self.embed(t) for t in texts])

class MockJobFetcher(JobFetcher):
    def __init__(self, jobs):
        self.jobs = {j.metadata.fingerprint: j for j in jobs}
    def get_by_fingerprint(self, fingerprint: str) -> JobPosting:
        return self.jobs.get(fingerprint)

def test_text_builder():
    from datetime import datetime, timezone
    job = JobPosting(
        id="123",
        title="Software Engineer",
        company="Stripe",
        location="Remote",
        skills=["Python", "SQL"],
        description="Testing description",
        url="http://test.com",
        raw_data={},
        metadata=RecordMetadata(
            source="test",
            pipeline_version="1",
            first_seen_at=datetime.now(timezone.utc),
            last_seen_at=datetime.now(timezone.utc)
        )
    )
    text = TextBuilder.build(job)
    assert "Software Engineer" in text
    assert "Company: Stripe" in text
    assert "Python" in text

def test_faiss_vector_store(tmp_path):
    store = FaissVectorStore(dimension=384)
    vectors = np.random.rand(3, 384).astype(np.float32)
    ids = ["id_1", "id_2", "id_3"]
    
    store.add(vectors, ids)
    assert store.count() == 3
    
    # search with same vector 1 should return id_1
    distances, results = store.search(np.expand_dims(vectors[0], axis=0), top_k=1)
    assert results[0][0] == "id_1"
    assert distances[0][0] == 0.0 # exact match L2 dist is 0

def test_embedding_cache(tmp_path):
    cache = EmbeddingCache(model_name="test_model", base_dir=str(tmp_path))
    vec = np.ones(384)
    cache.add("fingerprint_1", vec)
    cache.save()
    
    # Reload cache
    cache2 = EmbeddingCache(model_name="test_model", base_dir=str(tmp_path))
    assert cache2.get("fingerprint_1") is not None
    assert np.array_equal(cache2.get("fingerprint_1"), vec)
    assert cache2.get("missing") is None

def test_semantic_search_service():
    from datetime import datetime, timezone
    provider = MockEmbeddingProvider()
    store = FaissVectorStore(dimension=384)
    
    job = JobPosting(
        id="1",
        title="Test Job",
        company="Test Company",
        description="Test desc",
        url="http://test.com",
        raw_data={},
        metadata=RecordMetadata(
            fingerprint="hash1", 
            source="test",
            pipeline_version="1",
            first_seen_at=datetime.now(timezone.utc),
            last_seen_at=datetime.now(timezone.utc)
        )
    )
    fetcher = MockJobFetcher([job])
    
    # Add fake vector to store
    store.add(np.expand_dims(np.ones(384), axis=0), ["hash1"])
    
    service = SemanticSearchService(provider, store, fetcher)
    results = service.search("query string", top_k=1)
    
    assert len(results) == 1
    assert results[0][0].title == "Test Job"
    assert results[0][1] > 0.0 # similarity score

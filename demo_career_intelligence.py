import os
import json
import numpy as np
from typing import List

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
from src.domain.entities.job_posting import JobPosting
from src.intelligence.semantic_search.service import JobFetcher

from src.intelligence.skills.ontology import SkillOntology
from src.intelligence.skills.extractor import SkillExtractor

from src.intelligence.career.profiles.candidate import CandidateProfile
from src.intelligence.career.matching.matcher import SemanticMatcher
from src.intelligence.career.matching.models import RecommendationResult
from src.intelligence.career.explainability.engine import ExplainabilityEngine, MarketAssessor
from src.intelligence.career.transitions.graph import TransitionGraphGenerator
from src.intelligence.career.insights.engine import CareerInsightsEngine
from src.intelligence.career.evaluation.evaluator import RecommendationEvaluator
from src.intelligence.career.reports.generator import CareerReportRenderer

class InMemoryFetcher(JobFetcher):
    def __init__(self, jobs: List[JobPosting]):
        self.jobs_by_fp = {j.metadata.fingerprint: j for j in jobs if j.metadata and j.metadata.fingerprint}
        
    def get_by_fingerprint(self, fingerprint: str) -> JobPosting:
        return self.jobs_by_fp.get(fingerprint)

def main():
    print("========================================")
    print("JobPulse AI")
    print("Career Intelligence")
    print("========================================\n")
    
    # 1. Pipeline Setup (Mock Data Generation)
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
    
    # 2. Vector Store Setup
    embed_registry = EmbeddingRegistry()
    model_name = "all-MiniLM-L6-v2"
    provider = embed_registry.get_provider("sentence_transformer", model_name=model_name)
    cache = EmbeddingCache(model_name=model_name, base_dir="artifacts/embeddings")
    
    store = FaissVectorStore(dimension=384)
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
    
    if vectors:
        store.add(np.vstack(vectors), fps)
    cache.save()
    fetcher = InMemoryFetcher(processed_jobs)
    
    # 3. Candidate Setup
    candidate = CandidateProfile(
        skills=["Python", "FastAPI", "Docker", "SQL", "Git"],
        experience="Built scalable backend APIs and microservices for 3 years.",
        current_role="Backend Developer",
        years_experience=3.0,
        salary_expectation=110000.0,
        desired_roles=["Senior Backend Engineer", "Platform Engineer", "Data Engineer"],
    )
    
    print(f"Profile: {candidate.current_role}")
    print(f"Experience: {int(candidate.years_experience)} years\n")
    
    # 4. Engine Instantiations
    # Seed ontology to trigger skill extraction heuristically
    ontology = SkillOntology("config/skills.yaml")
    extractor = SkillExtractor(ontology)
    
    matcher = SemanticMatcher(provider, store, fetcher)
    explain_engine = ExplainabilityEngine(extractor)
    assessor = MarketAssessor()
    graph_gen = TransitionGraphGenerator()
    insights_engine = CareerInsightsEngine()
    evaluator = RecommendationEvaluator()
    report_gen = CareerReportRenderer()
    
    # 5. Execute Career Intelligence Pipeline
    matches = matcher.find_nearest_jobs(candidate, top_k=15)
    recommendations = explain_engine.explain(candidate, matches)
    market_score = assessor.assess(candidate, recommendations)
    transitions = graph_gen.generate(candidate, recommendations)
    insights = insights_engine.generate(recommendations, transitions)
    evaluation = evaluator.evaluate(recommendations, len(processed_jobs))
    
    result = RecommendationResult(
        recommendations=recommendations,
        transition_path=transitions,
        insights=insights,
        evaluation=evaluation
    )
    
    # 6. Console Output
    if recommendations:
        top_rec = recommendations[0]
        print(f"Top Recommendation: {top_rec.job.title}")
        print(f"Similarity: {top_rec.confidence:.2f}\n")
        
    print("Recommended Transition:")
    path = " -> ".join([candidate.current_role] + [e.to_role for e in transitions])
    print(path + "\n")
    
    if transitions:
        first_step = transitions[0]
        print("Priority Skills to Learn:")
        for skill in first_step.required_skills[:3]:
            print(f"- {skill}")
            
        print(f"Estimated Salary Increase: +{first_step.salary_delta_pct:.0f}%\n")
        
    print("Generating Report...")
    report_path = "artifacts/career_intelligence/candidate_report.md"
    report_gen.render(candidate, market_score, result, report_path)
    
    print("Done.")
    print("========================================")

if __name__ == "__main__":
    main()

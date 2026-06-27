import os
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
from src.intelligence.career.explainability.engine import ExplainabilityEngine

from src.intelligence.learning.graph import LearningGraph
from src.intelligence.learning.prioritizer import SkillPrioritizer
from src.intelligence.learning.impact import LearningImpactEngine
from src.intelligence.learning.curriculum import CurriculumGenerator
from src.intelligence.learning.synergy import SkillSynergyAnalyzer
from src.intelligence.learning.evaluation import LearningEvaluator
from src.intelligence.learning.planner import LearningPlanner
from src.intelligence.learning.reports import LearningReportRenderer

class InMemoryFetcher(JobFetcher):
    def __init__(self, jobs: List[JobPosting]):
        self.jobs_by_fp = {j.metadata.fingerprint: j for j in jobs if j.metadata and j.metadata.fingerprint}
        
    def get_by_fingerprint(self, fingerprint: str) -> JobPosting:
        return self.jobs_by_fp.get(fingerprint)

def main():
    print("========================================")
    print("JobPulse AI")
    print("Personalized Learning Intelligence")
    print("========================================\n")
    
    # 1. Pipeline Setup
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
    
    # 3. Base Intelligence Setup
    candidate = CandidateProfile(
        skills=["Python", "SQL", "Git"],
        experience="1 year building internal scripts.",
        current_role="Junior Developer",
        years_experience=1.0,
        salary_expectation=80000.0,
        desired_roles=["Backend Developer", "Data Engineer"],
    )
    
    print(f"Profile: {candidate.current_role}")
    print(f"Base Skills: {', '.join(candidate.skills)}\n")
    
    ontology = SkillOntology("config/skills.yaml")
    extractor = SkillExtractor(ontology)
    
    matcher = SemanticMatcher(provider, store, fetcher)
    explainer = ExplainabilityEngine(extractor)
    
    # 4. Learning Intelligence Setup
    graph = LearningGraph("config/learning_graph.yaml", "config/skill_metadata.yaml")
    prioritizer = SkillPrioritizer(graph)
    impact_engine = LearningImpactEngine(matcher, explainer)
    curriculum_gen = CurriculumGenerator(graph)
    synergy_analyzer = SkillSynergyAnalyzer(impact_engine, graph)
    evaluator = LearningEvaluator()
    
    planner = LearningPlanner(prioritizer, impact_engine, curriculum_gen, synergy_analyzer, evaluator)
    renderer = LearningReportRenderer()
    
    # 5. Execute
    print("Running initial matching...")
    initial_matches = matcher.find_nearest_jobs(candidate, top_k=20)
    initial_recs = explainer.explain(candidate, initial_matches)
    
    print("Generating Learning Plan and simulating opportunities...")
    plan = planner.generate_plan(candidate, initial_recs)
    
    # 6. Output
    if plan.skill_rois:
        top_skill = plan.skill_rois[0]
        print(f"\nTop Priority Skill: {top_skill.skill}")
        print(f"Rating: {top_skill.roi_rating} (Gain: +{top_skill.salary_gain_pct}%)")
        
    if plan.top_synergy:
        print(f"\nHighest ROI Synergy: {' + '.join(plan.top_synergy.skills)}")
        print(f"Unlocks {plan.top_synergy.jobs_unlocked} jobs (+{plan.top_synergy.salary_increase_pct}% Salary)")
        
    print(f"\nTotal Curriculum Estimated Effort: {plan.total_estimated_hours} hours")
    
    report_path = "artifacts/learning_intelligence/learning_roadmap.md"
    renderer.render(candidate, plan, report_path)
    print(f"Report generated at {report_path}")
    
    print("========================================")

if __name__ == "__main__":
    main()

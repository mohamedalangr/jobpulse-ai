import pytest
from datetime import datetime, timezone
from typing import Iterator, Dict, Any

from src.domain.entities.snapshot import MarketSnapshot, SnapshotMetadata, SnapshotBackend
from src.intelligence.trends.models import ConfidenceLevel, TrendDirection, TrendSeverity, SkillTrend
from src.intelligence.trends.detectors import SkillDemandDetector, EmergingTechnologyDetector
from src.intelligence.trends.analyzer import TrendAnalyzer

class MockBackend(SnapshotBackend):
    def __init__(self, jobs: int, skills: list):
        self._jobs = jobs
        self._skills = skills
        
    def stream_jobs(self) -> Iterator[Dict[str, Any]]:
        for i in range(self._jobs): yield {"id": i}
        
    def stream_skills(self) -> Iterator[Dict[str, Any]]:
        for s in self._skills: yield {"skill": s}
        
    def stream_companies(self) -> Iterator[Dict[str, Any]]: yield {}
    def stream_salaries(self) -> Iterator[Dict[str, Any]]: yield {}

def create_mock_snapshot(count: int, skills: list) -> MarketSnapshot:
    meta = SnapshotMetadata(
        snapshot_id="test", created_at=datetime.now(timezone.utc), dataset_version="1.0",
        scope="active", record_count=count, company_count=1, embedding_model="m",
        ontology_version="v", git_commit="c", schema_version="1.0"
    )
    return MarketSnapshot(metadata=meta, backend=MockBackend(count, skills))

def test_skill_demand_confidence_low_volume():
    # 2 -> 4 should be +100% relative but LOW confidence due to volume
    snap1 = create_mock_snapshot(100, ["Rust"]*2)
    snap2 = create_mock_snapshot(100, ["Rust"]*4)
    
    det = SkillDemandDetector()
    res = det.detect([snap1, snap2])
    
    rust_trend = next(t for t in res.findings if getattr(t, 'skill', None) == "Rust")
    assert rust_trend.relative_change_pct == 100.0
    assert rust_trend.confidence == ConfidenceLevel.LOW

def test_emerging_technology_rules():
    # Emerging criteria: Prev < 0.5% share, Curr > 1.0% share OR > 20 jobs, 
    # Relative growth > 50%, Absolute growth > 30, Confidence != LOW.
    
    snap1 = create_mock_snapshot(10000, ["Zig"]*20 + ["StableSkill"]*500)
    snap2 = create_mock_snapshot(10000, ["Zig"]*150 + ["StableSkill"]*510)
    
    det = EmergingTechnologyDetector()
    res = det.detect([snap1, snap2])
    
    # Zig should be detected as emerging
    assert len(res.findings) == 1
    assert res.findings[0].skill == "Zig"
    assert res.insights[0].confidence != ConfidenceLevel.LOW
    
def test_trend_analyzer_integration():
    snap1 = create_mock_snapshot(1000, ["Python"]*200)
    snap2 = create_mock_snapshot(1100, ["Python"]*250)
    
    analyzer = TrendAnalyzer()
    report = analyzer.analyze([snap1, snap2])
    
    assert report.skills is not None
    assert report.volatility is not None
    assert report.volatility.summary["growth_pct"] == 10.0
    assert len(report.executive_summary) > 0

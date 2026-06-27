import uuid
from typing import Sequence
from datetime import datetime

from src.domain.entities.snapshot import MarketSnapshot
from src.intelligence.trends.models import MarketTrendReport, TrendReportMetadata
from src.intelligence.trends.detectors import (
    MarketVolatilityDetector,
    SkillDemandDetector,
    EmergingTechnologyDetector,
    SalaryTrendDetector,
    CompanyGrowthDetector
)

class TrendAnalyzer:
    """
    Consumes a sequence of MarketSnapshots, passes them to individual independent Detectors,
    and aggregates their findings into a cohesive MarketTrendReport.
    """
    def __init__(self):
        self.detectors = [
            MarketVolatilityDetector(),
            SkillDemandDetector(),
            EmergingTechnologyDetector(),
            SalaryTrendDetector(),
            CompanyGrowthDetector()
        ]
        
    def analyze(self, snapshots: Sequence[MarketSnapshot]) -> MarketTrendReport:
        if len(snapshots) < 2:
            raise ValueError("Trend Analysis requires at least 2 snapshots to detect deltas.")
            
        results = {}
        all_insights = []
        
        for detector in self.detectors:
            res = detector.detect(snapshots)
            results[res.detector] = res
            all_insights.extend(res.insights)
            
        metadata = TrendReportMetadata(
            trend_id=str(uuid.uuid4()),
            generated_at=datetime.utcnow(),
            snapshot_range=[s.metadata.snapshot_id for s in snapshots],
            algorithm_version="1.0.0",
            normalization="market_share_percentile",
            confidence_model="v1_sample_persistence_magnitude"
        )
        
        return MarketTrendReport(
            metadata=metadata,
            volatility=results.get("MarketVolatilityDetector"),
            skills=results.get("SkillDemandDetector"),
            salaries=results.get("SalaryTrendDetector"),
            companies=results.get("CompanyGrowthDetector"),
            emerging_technologies=results.get("EmergingTechnologyDetector"),
            executive_summary=all_insights
        )

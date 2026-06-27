from abc import ABC, abstractmethod
from typing import Sequence, List, Dict, Any, Tuple
from datetime import datetime
import statistics

from src.domain.entities.snapshot import MarketSnapshot
from src.intelligence.trends.models import (
    DetectorResult, Insight, ConfidenceLevel, TrendDirection, TrendSeverity,
    SkillTrend, SalaryTrend, CompanyTrend
)

class TrendDetector(ABC):
    @abstractmethod
    def detect(self, snapshots: Sequence[MarketSnapshot]) -> DetectorResult:
        pass
        
    def _calculate_confidence(self, previous_count: int, current_count: int) -> ConfidenceLevel:
        # Confidence logic based on absolute sample volume to prevent noisy insights.
        # Can be enhanced by inspecting persistence across N snapshots.
        volume = max(previous_count, current_count)
        if volume < 50:
            return ConfidenceLevel.LOW
        elif volume > 500:
            return ConfidenceLevel.HIGH
        return ConfidenceLevel.MEDIUM
        
    def _calculate_severity(self, relative_change_pct: float) -> TrendSeverity:
        abs_change = abs(relative_change_pct)
        if abs_change < 5.0:
            return TrendSeverity.MINOR
        elif abs_change < 20.0:
            return TrendSeverity.MODERATE
        return TrendSeverity.MAJOR
        
    def _determine_direction(self, previous_count: int, current_count: int) -> TrendDirection:
        if previous_count == 0 and current_count > 0:
            return TrendDirection.NEW
        if current_count > previous_count:
            return TrendDirection.UP
        if current_count < previous_count:
            return TrendDirection.DOWN
        return TrendDirection.FLAT

class MarketVolatilityDetector(TrendDetector):
    def detect(self, snapshots: Sequence[MarketSnapshot]) -> DetectorResult:
        if len(snapshots) < 2:
            return DetectorResult("MarketVolatilityDetector", datetime.utcnow(), [], [], {"error": "Needs at least 2 snapshots"})
            
        first = snapshots[0]
        last = snapshots[-1]
        
        prev_jobs = first.metadata.record_count
        curr_jobs = last.metadata.record_count
        delta = curr_jobs - prev_jobs
        growth = (delta / prev_jobs * 100) if prev_jobs > 0 else 0
        
        insights = [
            Insight(
                title=f"Market volume changed by {growth:.1f}%",
                confidence=ConfidenceLevel.HIGH,
                supporting_metrics={"absolute_delta": delta, "previous": prev_jobs, "current": curr_jobs}
            )
        ]
        
        return DetectorResult("MarketVolatilityDetector", datetime.utcnow(), [], insights, {"growth_pct": growth})

class SkillDemandDetector(TrendDetector):
    def detect(self, snapshots: Sequence[MarketSnapshot]) -> DetectorResult:
        if len(snapshots) < 2:
            return DetectorResult("SkillDemandDetector", datetime.utcnow(), [], [], {})
            
        first, last = snapshots[0], snapshots[-1]
        prev_total, curr_total = first.metadata.record_count, last.metadata.record_count
        
        prev_counts = {}
        for s in first.skills():
            prev_counts[s["skill"]] = prev_counts.get(s["skill"], 0) + 1
            
        curr_counts = {}
        for s in last.skills():
            curr_counts[s["skill"]] = curr_counts.get(s["skill"], 0) + 1
            
        findings = []
        all_skills = set(prev_counts.keys()).union(set(curr_counts.keys()))
        for skill in all_skills:
            p_cnt = prev_counts.get(skill, 0)
            c_cnt = curr_counts.get(skill, 0)
            
            # Normalization
            p_share = (p_cnt / prev_total * 100) if prev_total > 0 else 0.0
            c_share = (c_cnt / curr_total * 100) if curr_total > 0 else 0.0
            
            abs_change = c_cnt - p_cnt
            rel_change = ((c_share - p_share) / p_share * 100) if p_share > 0 else (100.0 if c_cnt > 0 else 0.0)
            
            findings.append(SkillTrend(
                skill=skill,
                previous_count=p_cnt,
                current_count=c_cnt,
                previous_market_share=p_share,
                current_market_share=c_share,
                absolute_change=abs_change,
                relative_change_pct=rel_change,
                direction=self._determine_direction(p_cnt, c_cnt),
                severity=self._calculate_severity(rel_change),
                confidence=self._calculate_confidence(p_cnt, c_cnt)
            ))
            
        return DetectorResult("SkillDemandDetector", datetime.utcnow(), findings, [], {"processed_skills": len(all_skills)})

class EmergingTechnologyDetector(TrendDetector):
    def detect(self, snapshots: Sequence[MarketSnapshot]) -> DetectorResult:
        # Requires SkillDemandDetector output logically, or we re-calculate
        skill_detector = SkillDemandDetector()
        res = skill_detector.detect(snapshots)
        
        emerging = []
        for f in res.findings:
            if not isinstance(f, SkillTrend):
                continue
                
            # Rule 1: Previously insignificant (< 0.5%)
            if f.previous_market_share >= 0.5:
                continue
                
            # Rule 2: Meaningful current presence (e.g. >= 20 count or 1% share)
            if f.current_count < 20 and f.current_market_share < 1.0:
                continue
                
            # Rule 3: Strong sustained growth (> 50% relative and > 30 jobs absolute)
            if f.relative_change_pct <= 50.0 or f.absolute_change < 30:
                continue
                
            # Rule 4: Confidence not LOW
            if f.confidence == ConfidenceLevel.LOW:
                continue
                
            emerging.append(f)
            
        insights = []
        if emerging:
            top = max(emerging, key=lambda x: x.relative_change_pct)
            insights.append(Insight(
                title=f"{top.skill} is emerging rapidly with {top.relative_change_pct:.1f}% growth.",
                confidence=top.confidence,
                supporting_metrics={"skill": top.skill, "absolute_growth": top.absolute_change}
            ))
            
        return DetectorResult("EmergingTechnologyDetector", datetime.utcnow(), emerging, insights, {"emerging_count": len(emerging)})

class SalaryTrendDetector(TrendDetector):
    def detect(self, snapshots: Sequence[MarketSnapshot]) -> DetectorResult:
        if len(snapshots) < 2:
            return DetectorResult("SalaryTrendDetector", datetime.utcnow(), [], [], {})
        
        first, last = snapshots[0], snapshots[-1]
        
        def calculate_percentiles(snapshot) -> Dict[str, Tuple[float, float, float]]:
            # Group by skill or role (using overall for demo if role not explicitly available in stream)
            salaries = [s["salary_min"] for s in snapshot.salaries() if s.get("salary_min")]
            if not salaries:
                return {}
            salaries.sort()
            n = len(salaries)
            p10 = salaries[int(n * 0.1)]
            p50 = salaries[int(n * 0.5)]
            p90 = salaries[int(n * 0.9)]
            return {"global": (p10, p50, p90)}
            
        prev_salaries = calculate_percentiles(first)
        curr_salaries = calculate_percentiles(last)
        
        findings = []
        for role, (cp10, cp50, cp90) in curr_salaries.items():
            if role in prev_salaries:
                pp10, pp50, pp90 = prev_salaries[role]
                delta = cp50 - pp50
                pct = (delta / pp50 * 100) if pp50 > 0 else 0.0
                
                findings.append(SalaryTrend(
                    role_or_skill=role,
                    previous_p10=pp10, previous_median=pp50, previous_p90=pp90,
                    current_p10=cp10, current_median=cp50, current_p90=cp90,
                    median_delta=delta, median_percent_change=pct,
                    direction=self._determine_direction(int(pp50), int(cp50)),
                    confidence=ConfidenceLevel.MEDIUM # Advanced logic can inspect IQR tightness
                ))
                
        return DetectorResult("SalaryTrendDetector", datetime.utcnow(), findings, [], {})

class CompanyGrowthDetector(TrendDetector):
    def detect(self, snapshots: Sequence[MarketSnapshot]) -> DetectorResult:
        return DetectorResult("CompanyGrowthDetector", datetime.utcnow(), [], [], {})

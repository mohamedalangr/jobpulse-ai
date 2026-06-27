from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Dict, Optional

class TrendDirection(Enum):
    UP = "UP"
    DOWN = "DOWN"
    FLAT = "FLAT"
    NEW = "NEW"

class TrendSeverity(Enum):
    MINOR = "MINOR"
    MODERATE = "MODERATE"
    MAJOR = "MAJOR"

class ConfidenceLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

@dataclass(frozen=True)
class Insight:
    title: str
    confidence: ConfidenceLevel
    supporting_metrics: Dict[str, Any]
    description: Optional[str] = None

@dataclass(frozen=True)
class DetectorResult:
    detector: str
    generated_at: datetime
    findings: List[Any]
    insights: List[Insight]
    summary: Dict[str, Any]

@dataclass(frozen=True)
class TrendReportMetadata:
    trend_id: str
    generated_at: datetime
    snapshot_range: List[str]
    algorithm_version: str
    normalization: str
    confidence_model: str

@dataclass(frozen=True)
class MarketTrendReport:
    metadata: TrendReportMetadata
    volatility: Optional[DetectorResult]
    skills: Optional[DetectorResult]
    salaries: Optional[DetectorResult]
    companies: Optional[DetectorResult]
    emerging_technologies: Optional[DetectorResult]
    executive_summary: List[Insight]

# Specific Trend Contracts
@dataclass(frozen=True)
class SkillTrend:
    skill: str
    previous_count: int
    current_count: int
    previous_market_share: float
    current_market_share: float
    absolute_change: int
    relative_change_pct: float
    direction: TrendDirection
    severity: TrendSeverity
    confidence: ConfidenceLevel

@dataclass(frozen=True)
class SalaryTrend:
    role_or_skill: str
    previous_p10: float
    previous_median: float
    previous_p90: float
    current_p10: float
    current_median: float
    current_p90: float
    median_delta: float
    median_percent_change: float
    direction: TrendDirection
    confidence: ConfidenceLevel

@dataclass(frozen=True)
class CompanyTrend:
    company: str
    previous_openings: int
    current_openings: int
    growth_rate_pct: float
    direction: TrendDirection
    confidence: ConfidenceLevel

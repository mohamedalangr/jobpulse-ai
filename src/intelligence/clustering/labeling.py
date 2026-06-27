from dataclasses import dataclass
from typing import List
from abc import ABC, abstractmethod
from src.intelligence.clustering.summaries import ClusterSummary

@dataclass
class ClusterLabel:
    cluster_id: int
    label: str
    confidence: float
    evidence: List[str]

class ClusterLabeler(ABC):
    @abstractmethod
    def generate_label(self, summary: ClusterSummary) -> ClusterLabel:
        pass

class FrequencyClusterLabeler(ClusterLabeler):
    def generate_label(self, summary: ClusterSummary) -> ClusterLabel:
        # Heuristic approach:
        # If we have top titles, use the most common one.
        # Otherwise, use top skills.
        
        evidence = summary.top_titles[:2] + summary.top_skills[:3]
        
        if summary.top_titles:
            # Simple heuristic: Just use the most frequent title!
            best_title = summary.top_titles[0]
            label = best_title.title()
        elif summary.top_skills:
            label = f"{summary.top_skills[0].title()} Roles"
        else:
            label = f"Cluster {summary.cluster_id}"
            
        return ClusterLabel(
            cluster_id=summary.cluster_id,
            label=label,
            confidence=0.8, # Heuristics are fairly high confidence but not perfect
            evidence=evidence
        )

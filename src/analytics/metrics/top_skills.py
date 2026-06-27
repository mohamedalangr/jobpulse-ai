from typing import Any, List, Dict
from collections import Counter
from src.domain.entities.job_posting import JobPosting
from src.analytics.metrics.base import BaseMetric

class TopSkillsMetric(BaseMetric):
    @property
    def name(self) -> str:
        return "top_skills"

    def calculate(self, jobs: List[JobPosting]) -> List[Dict[str, Any]]:
        target_skills = ["python", "sql", "spark", "docker", "aws", "kubernetes", "react", "node"]
        skill_counter = Counter()
        
        for job in jobs:
            desc = (job.description or "").lower()
            skills = set([s.lower() for s in (job.skills or [])])
            
            for skill in target_skills:
                if skill in skills or skill in desc:
                    skill_counter[skill] += 1
                    
        return [{"skill": k, "count": v} for k, v in skill_counter.most_common(5)]

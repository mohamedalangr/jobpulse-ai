from typing import Any, Dict
from src.domain.entities.job_posting import JobPosting
from src.features.base import FeatureExtractor

class SkillsExtractor(FeatureExtractor):
    @property
    def namespace(self) -> str:
        return "skills"

    def extract(self, job: JobPosting) -> Dict[str, Any]:
        target_skills = ["python", "sql", "spark", "docker", "aws", "kubernetes", "react", "node"]
        
        # Fallback to checking description if skills array is empty
        skills = set([s.lower() for s in (job.skills or [])])
        desc = (job.description or "").lower()
        
        features = {}
        for skill in target_skills:
            has_skill = skill in skills or skill in desc
            features[skill] = has_skill
            
        features["count"] = len(skills) if skills else sum(features[s] for s in target_skills)
        return features

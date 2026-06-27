from typing import Any, Dict
from src.domain.entities.job_posting import JobPosting
from src.features.base import FeatureExtractor

class TitleExtractor(FeatureExtractor):
    @property
    def namespace(self) -> str:
        return "title"

    def extract(self, job: JobPosting) -> Dict[str, Any]:
        title = (job.title or "").lower()
        
        is_senior = any(term in title for term in ["senior", "sr", "sr.", "lead", "staff", "principal", "head"])
        is_manager = any(term in title for term in ["manager", "director", "vp", "president", "head"])
        is_junior = any(term in title for term in ["junior", "jr", "jr.", "entry", "associate"])
        
        return {
            "is_senior": is_senior,
            "is_manager": is_manager,
            "is_junior": is_junior
        }

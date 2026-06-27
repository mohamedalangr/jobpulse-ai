from typing import Any, Dict
from src.domain.entities.job_posting import JobPosting
from src.features.base import FeatureExtractor

class LocationExtractor(FeatureExtractor):
    @property
    def namespace(self) -> str:
        return "location"

    def extract(self, job: JobPosting) -> Dict[str, Any]:
        location = (job.location or "").lower()
        
        is_remote = "remote" in location or "anywhere" in location or "worldwide" in location
        
        return {
            "is_remote": is_remote,
            "country": job.country
        }

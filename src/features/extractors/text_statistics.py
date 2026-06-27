from typing import Any, Dict
import re
from src.domain.entities.job_posting import JobPosting
from src.features.base import FeatureExtractor

class TextStatisticsExtractor(FeatureExtractor):
    @property
    def namespace(self) -> str:
        return "description"

    def extract(self, job: JobPosting) -> Dict[str, Any]:
        text = job.description or ""
        
        char_count = len(text)
        words = text.split()
        word_count = len(words)
        
        sentence_count = len(re.split(r'[.!?]+', text)) - 1
        if sentence_count <= 0:
            sentence_count = 1 if word_count > 0 else 0
            
        readability_score = word_count / sentence_count if sentence_count > 0 else 0.0
        
        return {
            "char_count": char_count,
            "word_count": word_count,
            "sentence_count": sentence_count,
            "readability_score": readability_score
        }

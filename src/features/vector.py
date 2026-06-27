from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

@dataclass
class FeatureVector:
    job_id: str
    fingerprint: str
    version: str
    extracted_at: datetime
    features: Dict[str, Any]

import importlib
import pkgutil
import inspect
from datetime import datetime, timezone
from typing import List, Type
from src.domain.entities.job_posting import JobPosting
from src.features.base import FeatureExtractor
from src.features.vector import FeatureVector

class FeatureRegistry:
    def __init__(self, version: str = "v1"):
        self.version = version
        self._extractors: List[FeatureExtractor] = []

    def register(self, extractor: FeatureExtractor) -> None:
        self._extractors.append(extractor)

    def discover(self, package_name: str) -> None:
        """Dynamically load all FeatureExtractor classes from a package."""
        package = importlib.import_module(package_name)
        for _, module_name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
            if not is_pkg:
                module = importlib.import_module(module_name)
                for attr_name, attr in inspect.getmembers(module, inspect.isclass):
                    if issubclass(attr, FeatureExtractor) and attr is not FeatureExtractor:
                        if not any(isinstance(e, attr) for e in self._extractors):
                            self.register(attr())

    def extract_all(self, jobs: List[JobPosting]) -> List[FeatureVector]:
        vectors = []
        now = datetime.now(timezone.utc)
        
        for job in jobs:
            features = {}
            for extractor in self._extractors:
                raw_features = extractor.extract(job)
                namespace = extractor.namespace
                # Auto-prefix features
                for key, val in raw_features.items():
                    features[f"{namespace}.{key}"] = val
                    
            vectors.append(FeatureVector(
                job_id=job.id,
                fingerprint=job.metadata.fingerprint if job.metadata else "unknown",
                version=self.version,
                extracted_at=now,
                features=features
            ))
        return vectors

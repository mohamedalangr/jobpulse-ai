from abc import ABC, abstractmethod
from typing import List
from src.intelligence.semantic_search.service import JobFetcher

class LabelProvider(ABC):
    @abstractmethod
    def get_labels(self, fingerprints: List[str], fetcher: JobFetcher) -> List[str]:
        """Maps an ordered list of fingerprints to category strings."""
        pass

class CompanyLabelProvider(LabelProvider):
    def get_labels(self, fingerprints: List[str], fetcher: JobFetcher) -> List[str]:
        labels = []
        for fp in fingerprints:
            job = fetcher.get_by_fingerprint(fp)
            if job and job.company:
                labels.append(job.company)
            else:
                labels.append("Unknown")
        return labels

class RemoteLabelProvider(LabelProvider):
    def get_labels(self, fingerprints: List[str], fetcher: JobFetcher) -> List[str]:
        labels = []
        for fp in fingerprints:
            job = fetcher.get_by_fingerprint(fp)
            if job:
                loc = (job.location or "").lower()
                if "remote" in loc or "anywhere" in loc:
                    labels.append("Remote")
                else:
                    labels.append("On-site/Hybrid")
            else:
                labels.append("Unknown")
        return labels

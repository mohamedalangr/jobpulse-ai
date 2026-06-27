import logging
from src.processing.deduplication.store import DuplicateStore

logger = logging.getLogger("jobpulse_ai.deduplication")

class DuplicateDetector:
    """Uses a DuplicateStore to evaluate if a fingerprint has been seen."""
    def __init__(self, store: DuplicateStore):
        self.store = store

    def is_duplicate(self, fingerprint: str) -> bool:
        if not fingerprint:
            return False
            
        if self.store.exists(fingerprint):
            return True
            
        self.store.add(fingerprint)
        return False

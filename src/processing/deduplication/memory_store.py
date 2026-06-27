from src.processing.deduplication.store import DuplicateStore

class MemoryDuplicateStore(DuplicateStore):
    """In-memory set implementation of the DuplicateStore."""
    def __init__(self):
        self._seen = set()

    def exists(self, fingerprint: str) -> bool:
        return fingerprint in self._seen

    def add(self, fingerprint: str) -> None:
        self._seen.add(fingerprint)

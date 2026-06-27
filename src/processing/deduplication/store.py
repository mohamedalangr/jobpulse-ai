from abc import ABC, abstractmethod

class DuplicateStore(ABC):
    """Contract for a store that tracks seen job fingerprints."""
    @abstractmethod
    def exists(self, fingerprint: str) -> bool:
        pass

    @abstractmethod
    def add(self, fingerprint: str) -> None:
        pass

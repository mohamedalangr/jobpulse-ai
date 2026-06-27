from abc import ABC, abstractmethod
from typing import Dict, Any

class Provider(ABC):
    @abstractmethod
    def health(self) -> Dict[str, Any]:
        """Return provider health status and metadata."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Release underlying resources."""
        pass

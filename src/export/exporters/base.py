from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseExporter(ABC):
    @property
    @abstractmethod
    def extension(self) -> str:
        pass

    @abstractmethod
    def export(self, data: List[Dict[str, Any]], filepath: str) -> None:
        pass

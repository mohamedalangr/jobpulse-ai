from abc import ABC, abstractmethod
from src.application.context import RequestContext

class QueryHandler(ABC):
    @abstractmethod
    def execute(self, query: any, context: RequestContext) -> any:
        """Execute a read-only query without mutating state."""
        pass

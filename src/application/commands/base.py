from abc import ABC, abstractmethod
from src.application.context import RequestContext
from src.application.events.publisher import EventPublisher

class CommandHandler(ABC):
    def __init__(self, publisher: EventPublisher):
        self.publisher = publisher

    @abstractmethod
    def execute(self, command: any, context: RequestContext) -> any:
        """Execute a state-mutating command."""
        pass

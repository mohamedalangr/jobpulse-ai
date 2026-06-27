from dataclasses import dataclass, field
import time
import uuid

@dataclass
class Event:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    correlation_id: str = "unknown"

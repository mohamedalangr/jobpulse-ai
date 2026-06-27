from dataclasses import dataclass, field
import uuid
from typing import Optional
import time

@dataclass
class AnonymousUser:
    is_authenticated: bool = False
    username: str = "anonymous"

@dataclass
class RequestContext:
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    started_at: float = field(default_factory=time.time)
    user: any = field(default_factory=AnonymousUser)
    api_version: str = "v1"
    client_ip: Optional[str] = None

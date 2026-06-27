from dataclasses import dataclass, field
import uuid
from typing import Optional
import time
from src.security.principals import Principal, AnonymousPrincipal

@dataclass
class RequestContext:
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_id: Optional[str] = None
    principal: Principal = field(default_factory=AnonymousPrincipal)
    tenant_id: Optional[str] = None
    client_ip: str = "unknown"
    user_agent: str = "unknown"
    started_at: float = field(default_factory=time.time)
    api_version: str = "v1"

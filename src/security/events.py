from dataclasses import dataclass
from src.application.events.base import Event

@dataclass(kw_only=True)
class SecurityEvent(Event):
    principal_id: str
    authentication_type: str
    event_type: str
    resource: str
    outcome: str
    ip_address: str
    request_id: str

@dataclass(kw_only=True)
class AuthenticationSucceededEvent(SecurityEvent):
    event_type: str = "authentication_succeeded"

@dataclass(kw_only=True)
class AuthenticationFailedEvent(SecurityEvent):
    event_type: str = "authentication_failed"

@dataclass(kw_only=True)
class PermissionDeniedEvent(SecurityEvent):
    event_type: str = "permission_denied"

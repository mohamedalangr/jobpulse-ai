from dataclasses import dataclass, field
from typing import Set, Optional
from datetime import datetime
from abc import ABC

from src.security.permissions import Permission

@dataclass(frozen=True)
class Principal(ABC):
    principal_id: str
    display_name: str
    permissions: Set[Permission] = field(default_factory=set)
    tenant_id: Optional[str] = None
    authentication_type: str = "unknown"
    authenticated_at: Optional[datetime] = None

@dataclass(frozen=True)
class AnonymousPrincipal(Principal):
    principal_id: str = "anonymous"
    display_name: str = "Anonymous User"
    authentication_type: str = "none"

@dataclass(frozen=True)
class AuthenticatedPrincipal(Principal):
    # Enforces required fields for authenticated identity
    authentication_type: str = "api_key"

@dataclass(frozen=True)
class ServicePrincipal(Principal):
    principal_id: str = "system"
    display_name: str = "System Service"
    authentication_type: str = "internal"

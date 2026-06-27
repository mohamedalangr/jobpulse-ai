from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from fastapi import Request
import hmac
import hashlib
from datetime import datetime, timezone

from src.security.principals import Principal, AnonymousPrincipal, AuthenticatedPrincipal
from src.security.permissions import Permission
from src.application.config.settings import ConfigManager

@dataclass(frozen=True)
class AuthenticationResult:
    principal: Principal
    authenticated: bool
    failure_reason: Optional[str] = None

class AuthenticationProvider(ABC):
    @abstractmethod
    def authenticate(self, request: Request) -> AuthenticationResult:
        pass

class ApiKeyAuthenticationProvider(AuthenticationProvider):
    def __init__(self, config_manager: ConfigManager):
        self.expected_hash = config_manager.security_settings.api_key_hash

    def authenticate(self, request: Request) -> AuthenticationResult:
        api_key = request.headers.get("X-API-Key")
        
        # Omitted key -> Anonymous
        if not api_key:
            return AuthenticationResult(
                principal=AnonymousPrincipal(),
                authenticated=False
            )
            
        if not self.expected_hash:
            return AuthenticationResult(
                principal=AnonymousPrincipal(),
                authenticated=False,
                failure_reason="API key authentication not configured"
            )

        incoming_hash = hashlib.sha256(api_key.encode("utf-8")).hexdigest()
        
        if hmac.compare_digest(incoming_hash, self.expected_hash):
            principal = AuthenticatedPrincipal(
                principal_id="dev-admin",
                display_name="Development Administrator",
                permissions={
                    Permission.SEARCH, 
                    Permission.CAREER_ANALYSIS, 
                    Permission.LEARNING_PLAN, 
                    Permission.RUN_PIPELINE, 
                    Permission.VIEW_ANALYTICS, 
                    Permission.ADMIN
                },
                authentication_type="api_key",
                authenticated_at=datetime.now(timezone.utc)
            )
            return AuthenticationResult(
                principal=principal,
                authenticated=True
            )
            
        # Invalid key -> 401
        return AuthenticationResult(
            principal=AnonymousPrincipal(),
            authenticated=False,
            failure_reason="Invalid API Key"
        )

class IdentityResolver:
    def __init__(self, provider: AuthenticationProvider):
        self.provider = provider
        
    def resolve(self, request: Request) -> AuthenticationResult:
        return self.provider.authenticate(request)

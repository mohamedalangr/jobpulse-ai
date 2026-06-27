from fastapi import Request, Depends
from typing import Callable
import time

from src.security.principals import Principal
from src.security.policies import AuthorizationPolicy
from src.security.authentication import IdentityResolver, ApiKeyAuthenticationProvider
from src.api.exceptions import AuthenticationError, AuthorizationError
from src.security.events import AuthenticationFailedEvent, PermissionDeniedEvent
from src.application.events.publisher import EventPublisher

def get_event_publisher(request: Request) -> EventPublisher:
    return EventPublisher()

def get_identity_resolver(request: Request) -> IdentityResolver:
    config_manager = request.app.state.config_manager
    provider = ApiKeyAuthenticationProvider(config_manager)
    return IdentityResolver(provider)

def get_current_principal(
    request: Request,
    resolver: IdentityResolver = Depends(get_identity_resolver),
    publisher: EventPublisher = Depends(get_event_publisher)
) -> Principal:
    
    result = resolver.resolve(request)
    
    if not result.authenticated and result.failure_reason and result.failure_reason != "API key authentication not configured":
        publisher.publish(AuthenticationFailedEvent(
            timestamp=time.time(),
            request_id=getattr(request.state, "request_id", "unknown"),
            correlation_id=getattr(request.state, "correlation_id", "unknown"),
            principal_id="anonymous",
            authentication_type="api_key",
            resource=request.url.path,
            outcome="failure",
            ip_address=request.client.host if request.client else "unknown"
        ))
        raise AuthenticationError(result.failure_reason)
        
    request.state.principal = result.principal
    return result.principal

def require_policy(policy: AuthorizationPolicy) -> Callable:
    def policy_dependency(
        request: Request,
        principal: Principal = Depends(get_current_principal),
        publisher: EventPublisher = Depends(get_event_publisher)
    ):
        if not policy.evaluate(principal):
            publisher.publish(PermissionDeniedEvent(
                timestamp=time.time(),
                request_id=getattr(request.state, "request_id", "unknown"),
                correlation_id=getattr(request.state, "correlation_id", "unknown"),
                principal_id=principal.principal_id,
                authentication_type=principal.authentication_type,
                resource=request.url.path,
                outcome="denied",
                ip_address=request.client.host if request.client else "unknown"
            ))
            
            # If anonymous, escalate to 401 instead of 403
            if principal.authentication_type == "none":
                raise AuthenticationError("Authentication required.")
                
            raise AuthorizationError(policy.get_failure_reason())
            
        request.state.is_authenticated = True
        return principal
        
    return policy_dependency

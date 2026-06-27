from abc import ABC, abstractmethod
from typing import Optional
from src.security.principals import Principal
from src.security.permissions import Permission

class AuthorizationPolicy(ABC):
    @abstractmethod
    def evaluate(self, principal: Principal) -> bool:
        """Evaluate if the principal satisfies this policy."""
        pass

    @abstractmethod
    def get_failure_reason(self) -> str:
        """Returns the reason if evaluation fails."""
        pass

class PermissionPolicy(AuthorizationPolicy):
    def __init__(self, required_permission: Permission):
        self.required_permission = required_permission

    def evaluate(self, principal: Principal) -> bool:
        # Admin overrides all permission checks natively
        if Permission.ADMIN in principal.permissions:
            return True
        return self.required_permission in principal.permissions

    def get_failure_reason(self) -> str:
        return f"Missing required permission: {self.required_permission.value}"

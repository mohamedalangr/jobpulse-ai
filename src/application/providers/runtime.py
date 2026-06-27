from typing import Dict, Any, Optional

class RuntimeRegistry:
    """Stores instantiated singletons (loaded lazily)."""
    def __init__(self):
        self._instances: Dict[str, Any] = {}

    def register(self, key: str, instance: Any) -> None:
        self._instances[key] = instance

    def get(self, key: str) -> Optional[Any]:
        return self._instances.get(key)
        
    def clear(self) -> None:
        self._instances.clear()

_global_runtime_registry = RuntimeRegistry()

def get_runtime_registry() -> RuntimeRegistry:
    return _global_runtime_registry

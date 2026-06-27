from typing import Any, Dict
from src.application.providers.base import Provider
from src.application.uow import UnitOfWork

class DatabaseProvider(Provider):
    def __init__(self):
        self._connected = True

    def get_uow(self) -> UnitOfWork:
        class MockUoW(UnitOfWork):
            def begin(self): pass
            def commit(self): pass
            def rollback(self): pass
            def __enter__(self): return self
            def __exit__(self, exc_type, exc_val, exc_tb): pass
            
        return MockUoW()

    def health(self) -> Dict[str, Any]:
        return {
            "status": "up" if self._connected else "down"
        }

    def close(self) -> None:
        self._connected = False

def get_database_provider() -> DatabaseProvider:
    return DatabaseProvider()

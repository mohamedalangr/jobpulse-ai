import pytest
from fastapi import APIRouter, Depends, FastAPI
from fastapi.testclient import TestClient

from src.api.app import create_app
from src.security.permissions import Permission
from src.security.policies import PermissionPolicy
from src.api.dependencies import require_policy
from src.application.config.settings import ConfigManager
from src.api.schemas.responses import APIResponse
import time

# We construct a mock app that only includes a protected endpoint
app = create_app()

protected_router = APIRouter()

@protected_router.get("/protected", response_model=APIResponse[dict])
def protected_endpoint(principal = Depends(require_policy(PermissionPolicy(Permission.SEARCH)))):
    return APIResponse(
        success=True,
        request_id="test",
        timestamp=time.time(),
        data={"status": "ok"}
    )

app.include_router(protected_router, prefix="/api/v1")

def test_missing_api_key_returns_401():
    with TestClient(app) as client:
        response = client.get("/api/v1/protected")
        assert response.status_code == 401
        assert response.json()["error"]["code"] == "AUTHENTICATION_ERROR"
        assert response.json()["error"]["message"] == "Authentication required."

def test_invalid_api_key_returns_401():
    with TestClient(app) as client:
        response = client.get("/api/v1/protected", headers={"X-API-Key": "wrong-key"})
        assert response.status_code == 401
        assert response.json()["error"]["code"] == "AUTHENTICATION_ERROR"
        assert response.json()["error"]["message"] == "Invalid API Key"

def test_valid_api_key_returns_200():
    with TestClient(app) as client:
        response = client.get("/api/v1/protected", headers={"X-API-Key": "dev-secret-key"})
        assert response.status_code == 200
        assert response.json()["success"] is True

def test_security_headers_present():
    with TestClient(app) as client:
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.headers["X-Content-Type-Options"] == "nosniff"
        assert response.headers["Referrer-Policy"] == "no-referrer"
        assert response.headers["X-Frame-Options"] == "DENY"

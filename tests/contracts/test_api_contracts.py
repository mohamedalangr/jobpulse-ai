import pytest
from fastapi.testclient import TestClient
from src.api.app import create_app
from unittest.mock import patch

@pytest.fixture
def client():
    app = create_app()
    # Bypass heavy lifespan initialization for contract testing
    with TestClient(app) as test_client:
        yield test_client

def test_api_envelope_contract_health(client):
    """Ensures the core envelope schema remains stable across releases."""
    response = client.get("/api/v1/health/live")
    
    assert response.status_code == 200, "Expected 200 OK"
    data = response.json()
    
    # Contract rules
    assert "success" in data, "Envelope MUST contain 'success' flag"
    assert "request_id" in data, "Envelope MUST contain tracing 'request_id'"
    assert "timestamp" in data, "Envelope MUST contain 'timestamp'"
    assert "data" in data or "error" in data, "Envelope MUST contain 'data' payload or 'error'"
    
    assert data["success"] is True
    assert isinstance(data["data"], dict)
    assert "status" in data["data"]

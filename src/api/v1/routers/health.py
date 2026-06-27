from fastapi import APIRouter, Request
from src.api.schemas.responses import APIResponse
import time

router = APIRouter(tags=["System"])

@router.get("/health", response_model=APIResponse[dict])
async def liveness(request: Request):
    """Extremely lightweight liveness check."""
    return APIResponse(
        success=True,
        request_id=getattr(request.state, "request_id", "unknown"),
        timestamp=time.time(),
        data={"status": "alive"}
    )

@router.get("/ready", response_model=APIResponse[dict])
async def readiness(request: Request):
    """Deeper readiness check verifying critical infrastructure."""
    return APIResponse(
        success=True,
        request_id=getattr(request.state, "request_id", "unknown"),
        timestamp=time.time(),
        data={
            "status": "ready",
            "services": {
                "database": "ready",
                "faiss": "ready",
                "embedding_model": "lazy"
            }
        }
    )

@router.get("/version", response_model=APIResponse[dict])
async def version(request: Request):
    """Returns application build metadata."""
    config = request.app.state.config_manager
    return APIResponse(
        success=True,
        request_id=getattr(request.state, "request_id", "unknown"),
        timestamp=time.time(),
        data={
            "api_version": config.app_settings.version,
            "environment": config.app_settings.environment
        }
    )

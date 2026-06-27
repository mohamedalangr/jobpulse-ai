from fastapi import APIRouter, Request
from src.api.schemas.responses import APIResponse
import time
from fastapi.responses import JSONResponse

router = APIRouter(tags=["System"])

@router.get("/health/live", response_model=APIResponse[dict])
async def liveness(request: Request):
    """Extremely lightweight liveness check."""
    return APIResponse(
        success=True,
        request_id=getattr(request.state, "request_id", "unknown"),
        timestamp=time.time(),
        data={"status": "alive"}
    )

@router.get("/health/ready", response_model=APIResponse[dict])
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

@router.get("/health/startup", response_model=APIResponse[dict])
async def startup(request: Request):
    """Verifies that all startup tasks (like embedding preload) are fully completed."""
    is_complete = getattr(request.app.state, "startup_complete", False)
    if not is_complete:
        return JSONResponse(
            status_code=503,
            content=APIResponse(
                success=False,
                request_id=getattr(request.state, "request_id", "unknown"),
                timestamp=time.time(),
                error={"code": "STARTUP_IN_PROGRESS", "message": "Application is still starting up."}
            ).model_dump()
        )

    return APIResponse(
        success=True,
        request_id=getattr(request.state, "request_id", "unknown"),
        timestamp=time.time(),
        data={"status": "startup_complete"}
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

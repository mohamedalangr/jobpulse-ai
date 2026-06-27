from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import logging

logger = logging.getLogger("api")

class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        req_id = getattr(request.state, "request_id", "unknown")
        corr_id = getattr(request.state, "correlation_id", "unknown")
        proc_time = getattr(request.state, "process_time_ms", 0.0)
        
        logger.info(
            f"Request Complete",
            extra={
                "request_id": req_id,
                "correlation_id": corr_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": proc_time,
                "client": request.client.host if request.client else "unknown"
            }
        )
        return response

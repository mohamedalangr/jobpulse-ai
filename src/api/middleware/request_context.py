from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import uuid

class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        req_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        corr_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        
        request.state.request_id = req_id
        request.state.correlation_id = corr_id
        
        response = await call_next(request)
        
        response.headers["X-Request-ID"] = req_id
        response.headers["X-Correlation-ID"] = corr_id
        return response

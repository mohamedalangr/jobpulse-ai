from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import time

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        request.state.start_time = start_time
        
        response = await call_next(request)
        
        process_time_ms = (time.perf_counter() - start_time) * 1000
        response.headers["X-Process-Time"] = f"{process_time_ms:.2f}ms"
        request.state.process_time_ms = process_time_ms
        return response

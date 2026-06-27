from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from src.api.exceptions import JobPulseError
from src.api.schemas.responses import APIResponse, ErrorDetail
import time

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(JobPulseError)
    async def jobpulse_error_handler(request: Request, exc: JobPulseError):
        req_id = request.state.request_id if hasattr(request.state, "request_id") else "unknown"
        corr_id = request.state.correlation_id if hasattr(request.state, "correlation_id") else "unknown"
        
        err_detail = ErrorDetail(
            code=exc.code,
            message=exc.message,
            details=exc.details,
            correlation_id=corr_id
        )
        resp = APIResponse(
            success=False,
            request_id=req_id,
            timestamp=time.time(),
            error=err_detail
        )
        status_code = 500
        if exc.code == "VALIDATION_ERROR":
            status_code = 422
        elif exc.code == "AUTHENTICATION_ERROR":
            status_code = 401
        elif exc.code == "AUTHORIZATION_ERROR":
            status_code = 403
        elif exc.code == "SEARCH_ERROR":
            status_code = 400
            
        return JSONResponse(status_code=status_code, content=resp.model_dump())

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        req_id = request.state.request_id if hasattr(request.state, "request_id") else "unknown"
        corr_id = request.state.correlation_id if hasattr(request.state, "correlation_id") else "unknown"
        
        err_detail = ErrorDetail(
            code="VALIDATION_ERROR",
            message="Request validation failed.",
            details={"errors": exc.errors()},
            correlation_id=corr_id
        )
        resp = APIResponse(
            success=False,
            request_id=req_id,
            timestamp=time.time(),
            error=err_detail
        )
        return JSONResponse(status_code=422, content=resp.model_dump())

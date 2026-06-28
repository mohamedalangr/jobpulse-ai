from fastapi import FastAPI
from src.api.lifespan import lifespan
from src.api.exception_handlers import register_exception_handlers
from src.api.middleware.request_context import RequestContextMiddleware
from src.api.middleware.timing import TimingMiddleware
from src.api.middleware.logging import StructuredLoggingMiddleware
from src.api.middleware.security import SecurityHeadersMiddleware
from src.api.v1.routers import health, search

def create_app() -> FastAPI:
    app = FastAPI(
        title="JobPulse AI API",
        version="0.5.0",
        description="Career Intelligence Backend API",
        openapi_url="/api/v1/openapi.json",
        docs_url="/api/v1/docs",
        redoc_url="/api/v1/redoc",
        lifespan=lifespan
    )
    
    # Register Middleware (Note: FastAPI executes them bottom-up for outward flow)
    app.add_middleware(StructuredLoggingMiddleware)
    app.add_middleware(TimingMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RequestContextMiddleware)
    
    # Register Exception Handlers
    register_exception_handlers(app)
    
    # Register Routers
    app.include_router(health.router, prefix="/api/v1")
    app.include_router(search.router, prefix="/api/v1")
    
    
    return app

app = create_app()

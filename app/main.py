from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
import logging
import sys
from app.config import get_settings
from app.exceptions import (
    ErrorResponse,
    validation_exception_handler,
    sqlalchemy_exception_handler,
    generic_exception_handler
)
from app.routers.ce import router as ce_router
from app.routers.cpi import router as cpi_router
from app.routers.ppi import router as ppi_router
from app.routers.jt import router as jt_router
from app.routers.la import router as la_router
from app.routers.ci import router as ci_router
from app.routers.mp import router as mp_router
from app.routers.oe import router as oe_router
from app.routers.sa import router as sa_router
from app.routers.sm import router as sm_router

settings = get_settings()

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Rate limiter keyed by client IP; exempt health/root endpoints
limiter = Limiter(key_func=get_remote_address, default_limits=[settings.rate_limit])


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"Starting {settings.app_name}")
    logger.info(f"Debug mode: {settings.app_debug}")
    logger.info(f"Log level: {settings.log_level}")
    yield
    # Shutdown
    logger.info(f"Shutting down {settings.app_name}")


class APIKeyMiddleware(BaseHTTPMiddleware):
    # Paths that never require an API key
    EXEMPT_PATHS = {"/", "/health", "/docs", "/redoc", "/openapi.json"}

    async def dispatch(self, request: Request, call_next):
        # Skip auth for exempt paths
        if request.url.path in self.EXEMPT_PATHS:
            return await call_next(request)

        api_key = request.headers.get("X-API-Key") or request.query_params.get("api_key")
        valid_keys = [k.strip() for k in settings.api_keys.split(",") if k.strip()]
        
        if not valid_keys:
            return JSONResponse(
                status_code=503,
                content=ErrorResponse.build(
                    error_type="configuration_error",
                    message="API authentication is not configured.",
                    status_code=503,
                ),
            )
        
        if not api_key:
            return JSONResponse(
                status_code=401,
                content=ErrorResponse.build(
                    error_type="authentication_error",
                    message="API key required. Include X-API-Key header or api_key query parameter.",
                    status_code=401,
                ),
            )
        
        if api_key not in valid_keys:
            return JSONResponse(
                status_code=401,
                content=ErrorResponse.build(
                    error_type="authentication_error",
                    message="Invalid API key.",
                    status_code=401,
                ),
            )
        
        return await call_next(request)


app = FastAPI(
    title=settings.app_name,
    description="API for accessing Bureau of Labor Statistics economic data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(APIKeyMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ce_router, prefix="/api/v1/ce", tags=["Current Employment Statistics"])
app.include_router(cpi_router, prefix="/api/v1/cpi", tags=["Consumer Price Index"])
app.include_router(ppi_router, prefix="/api/v1/ppi", tags=["Producer Price Index"])
app.include_router(jt_router, prefix="/api/v1/jt", tags=["Job Openings & Labor Turnover"])
app.include_router(la_router, prefix="/api/v1/la", tags=["Local Area Unemployment"])
app.include_router(ci_router, prefix="/api/v1/ci", tags=["Employment Cost Index"])
app.include_router(mp_router, prefix="/api/v1/mp", tags=["Major Sector Productivity"])
app.include_router(oe_router, prefix="/api/v1/oe", tags=["Occupational Employment & Wages"])
app.include_router(sa_router, prefix="/api/v1/sa", tags=["State & Area Employment"])
app.include_router(sm_router, prefix="/api/v1/sm", tags=["State & Metropolitan Employment"])


@app.get("/", tags=["Root"])
@limiter.exempt
def root():
    return {
        "message": "BLS Economic Data API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
@limiter.exempt
def health_check():
    return {"status": "healthy"}

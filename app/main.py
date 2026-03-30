from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import sys
from app.config import get_settings
from app.exceptions import (
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


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        api_key = request.headers.get("X-API-Key") or request.query_params.get("api_key")
        valid_keys = [k.strip() for k in settings.api_keys.split(",") if k.strip()]
        
        if not valid_keys:
            return await call_next(request)
        
        if not api_key:
            raise HTTPException(status_code=401, detail="API key required. Include X-API-Key header or api_key query parameter.")
        
        if api_key not in valid_keys:
            raise HTTPException(status_code=401, detail="Invalid API key.")
        
        return await call_next(request)


app = FastAPI(
    title=settings.app_name,
    description="API for accessing Bureau of Labor Statistics economic data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

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
app.include_router(ci_router, prefix="/api/v1/ci", tags=["County Employment & Wages"])
app.include_router(mp_router, prefix="/api/v1/mp", tags=["Mass Layoff Statistics"])
app.include_router(oe_router, prefix="/api/v1/oe", tags=["Occupational Employment & Wages"])
app.include_router(sa_router, prefix="/api/v1/sa", tags=["State & Area Employment"])
app.include_router(sm_router, prefix="/api/v1/sm", tags=["State & Metropolitan Employment"])


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "BLS Economic Data API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}


@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.app_name}")
    logger.info(f"Debug mode: {settings.app_debug}")
    logger.info(f"Log level: {settings.log_level}")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.app_name}")

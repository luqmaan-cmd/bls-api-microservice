from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError, OperationalError, TimeoutError as SQLTimeoutError
import logging

logger = logging.getLogger(__name__)


class ErrorResponse:
    @staticmethod
    def build(error_type: str, message: str, status_code: int, details: dict = None):
        response = {
            "error": {
                "type": error_type,
                "message": message,
                "status_code": status_code
            }
        }
        if details:
            response["error"]["details"] = details
        return response


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    logger.warning(f"Validation error on {request.url.path}: {errors}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse.build(
            error_type="validation_error",
            message="Request validation failed",
            status_code=422,
            details={"errors": errors}
        )
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"Database error on {request.url.path}: {str(exc)}", exc_info=True)
    
    if isinstance(exc, OperationalError):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=ErrorResponse.build(
                error_type="database_connection_error",
                message="Unable to connect to database. Please try again later.",
                status_code=503
            )
        )
    
    if isinstance(exc, SQLTimeoutError):
        return JSONResponse(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            content=ErrorResponse.build(
                error_type="database_timeout",
                message="Database query timed out. Please refine your query or try again.",
                status_code=504
            )
        )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse.build(
            error_type="database_error",
            message="An unexpected database error occurred.",
            status_code=500
        )
    )


async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url.path}: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse.build(
            error_type="internal_error",
            message="An unexpected error occurred. Please try again later.",
            status_code=500
        )
    )

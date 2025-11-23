"""
Main entry point for the backend API.
"""

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.charts import router as charts_routers
from app.logger import logger

app = FastAPI(title="Hackathon API", description="API for the hackathon project")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler that catches all unhandled exceptions.
    Returns the error message as a string in the response.
    """
    # Get error message as string
    error_message = str(exc)
    error_type = type(exc).__name__

    # Log the full exception with traceback
    logger.error(
        f"Unhandled exception: {error_type} - {error_message}",
        exc_info=True,
        extra={
            "path": request.url.path,
            "method": request.method,
            "error_type": error_type,
            "error_message": error_message,
        },
    )

    # Return error as JSON with string message
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": error_type,
            "message": error_message,
            "detail": error_message,  # FastAPI standard field
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handle request validation errors (e.g., invalid request body).
    """
    error_message = str(exc)
    logger.warning(
        f"Validation error: {error_message}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "errors": exc.errors(),
        },
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "ValidationError",
            "message": error_message,
            "detail": exc.errors(),
        },
    )


app.include_router(charts_routers)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

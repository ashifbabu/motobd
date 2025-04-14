from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import get_redoc_html
import uvicorn
import os
from dotenv import load_dotenv
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Environment configuration
ENV = os.getenv("ENVIRONMENT", "development")
DEBUG = ENV == "development"
VERSION = "1.0.0"

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="RaiderCritic API",
        description="Your Trusted Motorcycle Review Platform",
        version=VERSION,
        debug=DEBUG,
        docs_url="/docs",
        redoc_url=None  # We'll create a custom redoc route
    )

    # Configure CORS
    origins = ["http://localhost:3000", "http://localhost:8000"] if DEBUG else ["https://raidercritic.com"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info("CORS middleware configured with origins: %s", origins)

    # Custom ReDoc route that works with Firebase hosting
    @app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url="/openapi.json",
            title=f"{app.title} - ReDoc",
            redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
        )

    # Exception handlers
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors(), "body": exc.body}
        )

    @app.get("/")
    async def root() -> Dict[str, Any]:
        """Root endpoint returning API information."""
        logger.info("Root endpoint called")
        return {
            "name": "RaiderCritic API",
            "version": VERSION,
            "environment": ENV,
            "status": "operational"
        }

    @app.get("/health")
    async def health_check() -> Dict[str, str]:
        """Health check endpoint for monitoring."""
        return {"status": "healthy"}

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    logger.info(f"Starting RaiderCritic API on port {port} in {ENV} mode")
    uvicorn.run(
        "main:app",
        host="0.0.0.0" if ENV == "production" else "127.0.0.1",
        port=port,
        reload=DEBUG,
        workers=4 if ENV == "production" else 1,
        log_level="info" if ENV == "production" else "debug"
    ) 
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
from datetime import datetime

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
        debug=DEBUG
    )

    # Configure CORS
    origins = ["*"]  # Allow all origins in Cloud Functions
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info("CORS middleware configured with origins: %s", origins)

    @app.get("/")
    async def root() -> Dict[str, Any]:
        """Root endpoint returning API information."""
        logger.info("Root endpoint called")
        return {
            "message": "Welcome to Bangla Motorcycle Review API",
            "version": VERSION,
            "status": "operational"
        }

    @app.get("/health")
    async def health_check() -> Dict[str, str]:
        """Health check endpoint for monitoring."""
        return {"status": "healthy"}

    return app

app = create_app()

# Don't run the server here, let Cloud Functions handle it
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    logger.info(f"Starting RaiderCritic API on port {port} in {ENV} mode")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    ) 
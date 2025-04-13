# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.api.routes.bikes import router as bikes_router
from app.api.routes.reviews import router as reviews_router
from app.api.routes.auth import router as auth_router
from app.api.routes.brands import router as brands_router
from app.api.routes.types import router as types_router
from app.api.routes.resources import router as resources_router

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Bangla Motorcycle Review API",
    description="API for managing motorcycle reviews in Bangla",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(bikes_router, prefix="/api/v1/bikes", tags=["bikes"])
app.include_router(reviews_router, prefix="/api/v1/reviews", tags=["reviews"])
app.include_router(brands_router, prefix="/api/v1/brands", tags=["brands"])
app.include_router(types_router, prefix="/api/v1/types", tags=["types"])
app.include_router(resources_router, prefix="/api/v1/resources", tags=["resources"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Bangla Motorcycle Review API"
    }

# Note: Other routers (brands, types, resources, auth) will be added later

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("API_HOST", "0.0.0.0"), port=int(os.getenv("API_PORT", 8000)))

#
#
# @https_fn.on_request()
# def on_request_example(req: https_fn.Request) -> https_fn.Response:
#     return https_fn.Response("Hello world!")
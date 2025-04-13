from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from app.models.schemas import Bike, BikeType, Resource, Review, ReviewCreate
from app.services.firebase_service import FirebaseService
from app.services.auth_service import AuthService
from app.services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["ai"])
firebase_service = FirebaseService()
auth_service = AuthService()
ai_service = AIService()
security = HTTPBearer()

@router.get("/bikes", response_model=List[Bike])
async def get_ai_bikes():
    bikes = await firebase_service.get_bikes()
    return bikes

@router.get("/bikes/{bike_id}", response_model=Bike)
async def get_ai_bike(bike_id: str):
    bike = await firebase_service.get_bike(bike_id)
    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")
    return bike

@router.get("/types", response_model=List[BikeType])
async def get_ai_bike_types():
    types = await firebase_service.get_bike_types()
    return types

@router.get("/types/{type_id}", response_model=BikeType)
async def get_ai_bike_type(type_id: str):
    bike_type = await firebase_service.get_bike_type(type_id)
    if not bike_type:
        raise HTTPException(status_code=404, detail="Bike type not found")
    return bike_type

@router.get("/resources", response_model=List[Resource])
async def get_ai_resources():
    resources = await firebase_service.get_resources()
    return resources

@router.get("/resources/{resource_id}", response_model=Resource)
async def get_ai_resource(resource_id: str):
    resource = await firebase_service.get_resource(resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

@router.post("/generate-review", response_model=ReviewCreate)
async def generate_review(
    bike_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        return await ai_service.generate_review(bike_id, credentials.credentials)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/analyze-review")
async def analyze_review(
    review_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        return await ai_service.analyze_review(review_id, credentials.credentials)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/summarize-reviews")
async def summarize_reviews(
    bike_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        return await ai_service.summarize_reviews(bike_id, credentials.credentials)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 
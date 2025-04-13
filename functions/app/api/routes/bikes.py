from fastapi import APIRouter, HTTPException, status, Request, Depends
from app.models.schemas import BikeCreate, Bike, ReviewCreate, Review
from app.services.firebase_service import FirebaseService
from app.services.auth_service import AuthService
from typing import List
from datetime import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()

def get_firebase_service(request: Request) -> FirebaseService:
    instance_id = getattr(request.app.state, "firebase_instance_id", "default")
    return FirebaseService.get_instance(instance_id)

def get_auth_service(request: Request) -> AuthService:
    instance_id = getattr(request.app.state, "firebase_instance_id", "default")
    return AuthService(instance_id)

@router.get("/", response_model=List[Bike])
async def get_bikes(request: Request):
    firebase_service = get_firebase_service(request)
    return await firebase_service.get_bikes()

@router.post("/", response_model=Bike, status_code=status.HTTP_201_CREATED)
async def create_bike(bike: BikeCreate, request: Request):
    firebase_service = get_firebase_service(request)
    return await firebase_service.create_bike(bike.model_dump(), "test_user")

@router.get("/{bike_id}", response_model=Bike)
async def get_bike(bike_id: str, request: Request):
    firebase_service = get_firebase_service(request)
    bike = await firebase_service.get_bike(bike_id)
    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")
    return bike

@router.put("/{bike_id}", response_model=Bike)
async def update_bike(bike_id: str, bike: BikeCreate, request: Request):
    firebase_service = get_firebase_service(request)
    updated_bike = await firebase_service.update_bike(bike_id, bike.model_dump(), "test_user")
    if not updated_bike:
        raise HTTPException(status_code=404, detail="Bike not found")
    return updated_bike

@router.delete("/{bike_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bike(bike_id: str, request: Request):
    firebase_service = get_firebase_service(request)
    deleted = await firebase_service.delete_bike(bike_id, "test_user")
    if not deleted:
        raise HTTPException(status_code=404, detail="Bike not found")
    return None

@router.get("/{bike_id}/reviews", response_model=List[Review])
async def get_bike_reviews(bike_id: str, request: Request):
    firebase_service = get_firebase_service(request)
    bike = await firebase_service.get_bike(bike_id)
    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")
    return await firebase_service.get_bike_reviews(bike_id)

@router.post("/{bike_id}/reviews", response_model=Review, status_code=status.HTTP_201_CREATED)
async def create_bike_review(
    bike_id: str,
    review: ReviewCreate,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    firebase_service = get_firebase_service(request)
    auth_service = get_auth_service(request)

    bike = await firebase_service.get_bike(bike_id)
    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")

    current_user = await auth_service.get_current_user(credentials.credentials)
    review_data = review.model_dump()
    review_data["bike_id"] = bike_id
    return await firebase_service.create_review(review_data, current_user.id)

@router.get("/{bike_id}/reviews/{review_id}", response_model=Review)
async def get_bike_review(bike_id: str, review_id: str, request: Request):
    firebase_service = get_firebase_service(request)
    bike = await firebase_service.get_bike(bike_id)
    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")
    review = await firebase_service.get_review(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if review.bike_id != bike_id:
        raise HTTPException(status_code=404, detail="Review not found for this bike")
    return review 
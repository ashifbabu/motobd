from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.schemas import BikeType
from app.services.firebase_service import FirebaseService

router = APIRouter()
firebase_service = FirebaseService()

@router.get("/", response_model=List[BikeType])
async def get_types():
    return await firebase_service.get_bike_types()

@router.get("/{type_id}", response_model=BikeType)
async def get_type(type_id: str):
    bike_type = await firebase_service.get_bike_type(type_id)
    if not bike_type:
        raise HTTPException(status_code=404, detail="Type not found")
    return bike_type 
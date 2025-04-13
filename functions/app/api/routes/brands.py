from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.schemas import Brand
from app.services.firebase_service import FirebaseService

router = APIRouter()
firebase_service = FirebaseService()

@router.get("/", response_model=List[Brand])
async def get_brands():
    return await firebase_service.get_brands()

@router.get("/{brand_id}", response_model=Brand)
async def get_brand(brand_id: str):
    brand = await firebase_service.get_brand(brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand 
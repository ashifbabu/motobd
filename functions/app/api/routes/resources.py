from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.schemas import Resource
from app.services.firebase_service import FirebaseService

router = APIRouter()
firebase_service = FirebaseService()

@router.get("/", response_model=List[Resource])
async def get_resources():
    return await firebase_service.get_resources()

@router.get("/{resource_id}", response_model=Resource)
async def get_resource(resource_id: str):
    resource = await firebase_service.get_resource(resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource 
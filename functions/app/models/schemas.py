from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict
from datetime import datetime

class BikeBase(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    name: str
    brand: str
    model: str
    year: int = Field(..., description="Year of the bike model")
    type: str
    description: str
    price: float
    specs: Dict[str, str]

class BikeCreate(BikeBase):
    pass

class Bike(BikeBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ReviewBase(BaseModel):
    bike_id: str
    title: str
    content: str
    rating: float = Field(..., ge=0, le=5)
    pros: List[str]
    cons: List[str]

class ReviewCreate(ReviewBase):
    user_id: str = Field(..., description="ID of the user creating the review")

class Review(ReviewCreate):
    id: str = Field(..., description="Unique identifier for the review")
    created_at: datetime = Field(..., description="Timestamp when the review was created")
    updated_at: datetime = Field(..., description="Timestamp when the review was last updated")

class UserBase(BaseModel):
    name: str
    email: str
    role: str = "user"

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    favorites: List[str] = []

    class Config:
        from_attributes = True

class Brand(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BikeType(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Resource(BaseModel):
    id: str
    title: str
    content: str
    type: str
    url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 
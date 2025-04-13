from fastapi import APIRouter, HTTPException, status, Request, Depends
from app.models.schemas import ReviewCreate, Review
from app.services.firebase_service import FirebaseService
from app.services.auth_service import AuthService
from typing import List
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()

def get_firebase_service(request: Request) -> FirebaseService:
    instance_id = getattr(request.app.state, "firebase_instance_id", "default")
    return FirebaseService.get_instance(instance_id)

def get_auth_service(request: Request) -> AuthService:
    instance_id = getattr(request.app.state, "firebase_instance_id", "default")
    return AuthService(instance_id)

@router.get("/user/{user_id}", response_model=List[Review])
async def get_user_reviews(
    user_id: str,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    firebase_service = get_firebase_service(request)
    auth_service = get_auth_service(request)

    if user_id == "me":
        current_user = await auth_service.get_current_user(credentials.credentials)
        user_id = current_user.id

    reviews = [review for review in await firebase_service.get_reviews() if review.user_id == user_id]
    return reviews

@router.get("/", response_model=List[Review])
async def get_reviews(request: Request):
    firebase_service = get_firebase_service(request)
    return await firebase_service.get_reviews()

@router.post("/", response_model=Review, status_code=status.HTTP_201_CREATED)
async def create_review(review: ReviewCreate, request: Request):
    firebase_service = get_firebase_service(request)
    return await firebase_service.create_review(review.model_dump(), "test_user")

@router.get("/{review_id}", response_model=Review)
async def get_review(review_id: str, request: Request):
    firebase_service = get_firebase_service(request)
    review = await firebase_service.get_review(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.put("/{review_id}", response_model=Review)
async def update_review(review_id: str, review: ReviewCreate, request: Request):
    firebase_service = get_firebase_service(request)
    updated_review = await firebase_service.update_review(review_id, review.model_dump(), "test_user")
    if not updated_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return updated_review

@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(review_id: str, request: Request):
    firebase_service = get_firebase_service(request)
    deleted = await firebase_service.delete_review(review_id, "test_user")
    if not deleted:
        raise HTTPException(status_code=404, detail="Review not found")
    return None

# AI Generation endpoints
@router.post("/ai/generate/review")
async def generate_review(bike_id: str):
    # TODO: Implement AI review generation
    raise HTTPException(status_code=501, detail="AI review generation not implemented yet")

@router.post("/ai/generate/summary")
async def generate_summary(bike_id: str):
    # TODO: Implement AI summary generation
    raise HTTPException(status_code=501, detail="AI summary generation not implemented yet")

@router.post("/ai/generate/comparison")
async def generate_comparison(bike_ids: List[str]):
    # TODO: Implement AI comparison generation
    raise HTTPException(status_code=501, detail="AI comparison generation not implemented yet") 
from typing import List, Dict
from datetime import datetime
import uuid
from ..models.schemas import Review, ReviewCreate

class ReviewService:
    def __init__(self):
        self.reviews: Dict[str, Review] = {}

    def get_reviews(self) -> List[Review]:
        """Get all reviews."""
        return list(self.reviews.values())

    def get_review(self, review_id: str) -> Review:
        """Get a specific review by ID."""
        if review_id not in self.reviews:
            raise ValueError(f"Review with ID {review_id} not found")
        return self.reviews[review_id]

    def create_review(self, review: ReviewCreate) -> Review:
        """Create a new review."""
        review_id = str(uuid.uuid4())
        now = datetime.utcnow()
        new_review = Review(
            id=review_id,
            created_at=now,
            updated_at=now,
            **review.dict()
        )
        self.reviews[review_id] = new_review
        return new_review

    def update_review(self, review_id: str, review: ReviewCreate) -> Review:
        """Update an existing review."""
        if review_id not in self.reviews:
            raise ValueError(f"Review with ID {review_id} not found")
        
        existing_review = self.reviews[review_id]
        updated_review = Review(
            id=review_id,
            created_at=existing_review.created_at,
            updated_at=datetime.utcnow(),
            **review.dict()
        )
        self.reviews[review_id] = updated_review
        return updated_review

    def delete_review(self, review_id: str) -> None:
        """Delete a review."""
        if review_id not in self.reviews:
            raise ValueError(f"Review with ID {review_id} not found")
        del self.reviews[review_id]

    def get_user_reviews(self, user_id: str) -> List[Review]:
        """Get all reviews by a specific user."""
        return [review for review in self.reviews.values() if review.user_id == user_id] 
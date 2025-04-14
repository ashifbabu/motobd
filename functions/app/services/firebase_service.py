from datetime import datetime
from typing import Dict, List, Optional
from .firebase_init import get_firestore_client

class FirebaseService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseService, cls).__new__(cls)
            cls._instance.db = get_firestore_client()
        return cls._instance

    def get_bikes(self) -> List[Dict]:
        """Get all bikes from Firestore."""
        bikes_ref = self.db.collection('bikes')
        docs = bikes_ref.stream()
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]

    def get_bike(self, bike_id: str) -> Optional[Dict]:
        """Get a specific bike by ID."""
        doc = self.db.collection('bikes').document(bike_id).get()
        if doc.exists:
            return {"id": doc.id, **doc.to_dict()}
        return None

    def create_bike(self, bike_data: Dict) -> str:
        """Create a new bike document."""
        bike_data["created_at"] = datetime.utcnow()
        bike_data["updated_at"] = datetime.utcnow()
        doc_ref = self.db.collection('bikes').document()
        doc_ref.set(bike_data)
        return doc_ref.id

    def update_bike(self, bike_id: str, bike_data: Dict) -> bool:
        """Update an existing bike document."""
        bike_ref = self.db.collection('bikes').document(bike_id)
        if bike_ref.get().exists:
            bike_data["updated_at"] = datetime.utcnow()
            bike_ref.update(bike_data)
            return True
        return False

    def delete_bike(self, bike_id: str) -> bool:
        """Delete a bike document."""
        bike_ref = self.db.collection('bikes').document(bike_id)
        if bike_ref.get().exists:
            bike_ref.delete()
            return True
        return False

    def get_reviews(self, bike_id: Optional[str] = None) -> List[Dict]:
        """Get all reviews or reviews for a specific bike."""
        reviews_ref = self.db.collection('reviews')
        if bike_id:
            reviews_ref = reviews_ref.where('bike_id', '==', bike_id)
        docs = reviews_ref.stream()
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]

    def get_review(self, review_id: str) -> Optional[Dict]:
        """Get a specific review by ID."""
        doc = self.db.collection('reviews').document(review_id).get()
        if doc.exists:
            return {"id": doc.id, **doc.to_dict()}
        return None

    def create_review(self, review_data: Dict) -> str:
        """Create a new review document."""
        review_data["created_at"] = datetime.utcnow()
        review_data["updated_at"] = datetime.utcnow()
        doc_ref = self.db.collection('reviews').document()
        doc_ref.set(review_data)
        return doc_ref.id

    def update_review(self, review_id: str, review_data: Dict) -> bool:
        """Update an existing review document."""
        review_ref = self.db.collection('reviews').document(review_id)
        if review_ref.get().exists:
            review_data["updated_at"] = datetime.utcnow()
            review_ref.update(review_data)
            return True
        return False

    def delete_review(self, review_id: str) -> bool:
        """Delete a review document."""
        review_ref = self.db.collection('reviews').document(review_id)
        if review_ref.get().exists:
            review_ref.delete()
            return True
        return False 
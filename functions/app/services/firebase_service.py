from datetime import datetime
from typing import List, Optional
from app.models.schemas import Bike, BikeType, Brand, Resource, Review, User

class FirebaseService:
    _instances = {}

    @classmethod
    def get_instance(cls, instance_id: str = "default"):
        if instance_id not in cls._instances:
            cls._instances[instance_id] = cls()
        return cls._instances[instance_id]

    @classmethod
    def clear_instance(cls, instance_id: str = "default"):
        if instance_id in cls._instances:
            del cls._instances[instance_id]

    def __init__(self):
        # Mock data for testing
        self.bikes = {}
        self.reviews = {}
        self.brands = {}
        self.types = {}
        self.resources = {}
        self.users = {}

    async def get_bikes(self) -> List[Bike]:
        return list(self.bikes.values())

    async def get_bike(self, bike_id: str) -> Optional[Bike]:
        return self.bikes.get(bike_id)

    async def create_bike(self, bike_data: dict, user_id: str) -> Bike:
        bike_id = f"bike_{len(self.bikes) + 1}"
        bike = Bike(
            id=bike_id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            **bike_data
        )
        self.bikes[bike_id] = bike
        return bike

    async def update_bike(self, bike_id: str, bike_data: dict, user_id: str) -> Optional[Bike]:
        if bike_id not in self.bikes:
            return None
        bike = Bike(
            id=bike_id,
            created_at=self.bikes[bike_id].created_at,
            updated_at=datetime.now(),
            **bike_data
        )
        self.bikes[bike_id] = bike
        return bike

    async def delete_bike(self, bike_id: str, user_id: str) -> bool:
        if bike_id not in self.bikes:
            return False
        del self.bikes[bike_id]
        return True

    async def get_reviews(self) -> List[Review]:
        return list(self.reviews.values())

    async def get_review(self, review_id: str) -> Optional[Review]:
        return self.reviews.get(review_id)

    async def create_review(self, review_data: dict, user_id: str) -> Review:
        review_id = f"review_{len(self.reviews) + 1}"
        # Remove user_id from review_data if it exists
        if "user_id" in review_data:
            del review_data["user_id"]
        review = Review(
            id=review_id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            user_id=user_id,
            **review_data
        )
        self.reviews[review_id] = review
        return review

    async def update_review(self, review_id: str, review_data: dict, user_id: str) -> Optional[Review]:
        if review_id not in self.reviews:
            return None
        review = Review(
            id=review_id,
            created_at=self.reviews[review_id].created_at,
            updated_at=datetime.now(),
            user_id=user_id,
            **review_data
        )
        self.reviews[review_id] = review
        return review

    async def delete_review(self, review_id: str, user_id: str) -> bool:
        if review_id not in self.reviews:
            return False
        del self.reviews[review_id]
        return True

    async def get_brands(self) -> List[Brand]:
        return list(self.brands.values())

    async def get_brand(self, brand_id: str) -> Optional[Brand]:
        return self.brands.get(brand_id)

    async def get_bike_types(self) -> List[BikeType]:
        return list(self.types.values())

    async def get_bike_type(self, type_id: str) -> Optional[BikeType]:
        return self.types.get(type_id)

    async def get_resources(self) -> List[Resource]:
        return list(self.resources.values())

    async def get_resource(self, resource_id: str) -> Optional[Resource]:
        return self.resources.get(resource_id)

    async def get_user(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

    async def create_user(self, user_data: dict) -> User:
        user_id = f"user_{len(self.users) + 1}"
        user = User(
            id=user_id,
            **user_data
        )
        self.users[user_id] = user
        return user

    async def update_user(self, user_id: str, user_data: dict) -> Optional[User]:
        if user_id not in self.users:
            return None
        user = User(
            id=user_id,
            created_at=self.users[user_id].created_at,
            **user_data
        )
        self.users[user_id] = user
        return user

    async def delete_user(self, user_id: str) -> bool:
        if user_id not in self.users:
            return False
        del self.users[user_id]
        return True

    async def get_bike_reviews(self, bike_id: str) -> List[Review]:
        return [review for review in self.reviews.values() if review.bike_id == bike_id] 
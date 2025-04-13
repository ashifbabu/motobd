from datetime import datetime
from typing import List, Dict
import uuid
from app.models.schemas import Bike, BikeCreate

class BikeService:
    def __init__(self):
        self.bikes: Dict[str, dict] = {}  # In-memory storage for testing

    async def get_bikes(self) -> List[Bike]:
        try:
            return [Bike(**bike_data) for bike_data in self.bikes.values()]
        except Exception as e:
            raise Exception(f"Error getting bikes: {str(e)}")

    async def get_bike(self, bike_id: str) -> Bike:
        try:
            if bike_id not in self.bikes:
                raise Exception("Bike not found")
            return Bike(**self.bikes[bike_id])
        except Exception as e:
            raise Exception(f"Error getting bike: {str(e)}")

    async def create_bike(self, bike: BikeCreate, user_token: str) -> Bike:
        try:
            bike_id = str(uuid.uuid4())
            bike_data = bike.model_dump()
            bike_data['id'] = bike_id
            bike_data['created_at'] = datetime.utcnow()
            bike_data['updated_at'] = datetime.utcnow()
            
            self.bikes[bike_id] = bike_data
            
            return Bike(**bike_data)
        except Exception as e:
            raise Exception(f"Error creating bike: {str(e)}")

    async def update_bike(self, bike_id: str, bike: BikeCreate, user_token: str) -> Bike:
        try:
            if bike_id not in self.bikes:
                raise Exception("Bike not found")
            
            bike_data = bike.model_dump()
            bike_data['id'] = bike_id
            bike_data['created_at'] = self.bikes[bike_id]['created_at']
            bike_data['updated_at'] = datetime.utcnow()
            
            self.bikes[bike_id] = bike_data
            
            return Bike(**bike_data)
        except Exception as e:
            raise Exception(f"Error updating bike: {str(e)}")

    async def delete_bike(self, bike_id: str, user_token: str) -> None:
        try:
            if bike_id not in self.bikes:
                raise Exception("Bike not found")
            
            del self.bikes[bike_id]
        except Exception as e:
            raise Exception(f"Error deleting bike: {str(e)}")

    async def search_bikes(self, query: str) -> List[Bike]:
        try:
            bikes = []
            for bike_data in self.bikes.values():
                if query.lower() in bike_data['name'].lower() or query.lower() in bike_data['brand'].lower():
                    bikes.append(Bike(**bike_data))
            return bikes
        except Exception as e:
            raise Exception(f"Error searching bikes: {str(e)}")

    async def filter_bikes(self, brand: str = None, type: str = None) -> List[Bike]:
        try:
            bikes = []
            for bike_data in self.bikes.values():
                if (not brand or bike_data['brand'] == brand) and (not type or bike_data['type'] == type):
                    bikes.append(Bike(**bike_data))
            return bikes
        except Exception as e:
            raise Exception(f"Error filtering bikes: {str(e)}")

    async def get_bike_reviews(self, bike_id: str) -> List[dict]:
        try:
            if bike_id not in self.bikes:
                raise Exception("Bike not found")
            # For testing, return an empty list
            return []
        except Exception as e:
            raise Exception(f"Error getting bike reviews: {str(e)}")

    async def create_bike_review(self, bike_id: str, review_data: dict, user_token: str) -> dict:
        try:
            if bike_id not in self.bikes:
                raise Exception("Bike not found")
            
            review_id = str(uuid.uuid4())
            review = {
                **review_data.model_dump(),
                'id': review_id,
                'bike_id': bike_id,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
                'author': user_token
            }
            
            return review
        except Exception as e:
            raise Exception(f"Error creating bike review: {str(e)}") 
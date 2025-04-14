from datetime import datetime
from typing import List, Optional
from app.models.schemas import Bike, BikeType, Brand, Resource, Review, User
from firebase_admin import firestore, initialize_app, credentials, get_app, delete_app
import os

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
        try:
            # Try to get existing app
            app = get_app()
            delete_app(app)
        except ValueError:
            pass

        try:
            # Try to initialize with service account file
            service_account_path = os.path.join(os.path.dirname(__file__), '..', '..', 'firebase-service-account.json')
            if os.path.exists(service_account_path):
                cred = credentials.Certificate(service_account_path)
            else:
                # Fallback to environment variables
                cred_dict = {
                    "type": "service_account",
                    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
                    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
                    "private_key": os.getenv("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n"),
                    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
                    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_CERT_URL")
                }
                cred = credentials.Certificate(cred_dict)
            
            initialize_app(cred, {
                'projectId': os.getenv('FIREBASE_PROJECT_ID')
            })
        except Exception as e:
            print(f"Warning: Could not initialize Firebase with credentials: {e}")
            print("Falling back to application default credentials")
            cred = credentials.ApplicationDefault()
            initialize_app(cred, {
                'projectId': os.getenv('FIREBASE_PROJECT_ID')
            })

        self.db = firestore.client()
        # Mock data for testing
        self.bikes = {}
        self.reviews = {}
        self.brands = {}
        self.types = {}
        self.resources = {}
        self.users = {}

    async def get_bikes(self) -> List[Bike]:
        bikes_ref = self.db.collection('bikes')
        bikes = []
        for doc in bikes_ref.stream():
            bike_data = doc.to_dict()
            bike_data['id'] = doc.id
            bikes.append(Bike(**bike_data))
        return bikes

    async def get_bike(self, bike_id: str) -> Optional[Bike]:
        bike_ref = self.db.collection('bikes').document(bike_id)
        bike_doc = bike_ref.get()
        if bike_doc.exists:
            bike_data = bike_doc.to_dict()
            bike_data['id'] = bike_id
            return Bike(**bike_data)
        return None

    async def create_bike(self, bike_data: dict, user_id: str) -> Bike:
        bike_data['created_at'] = datetime.now()
        bike_data['updated_at'] = datetime.now()
        bike_data['user_id'] = user_id
        
        bike_ref = self.db.collection('bikes').document()
        bike_ref.set(bike_data)
        
        bike_data['id'] = bike_ref.id
        return Bike(**bike_data)

    async def update_bike(self, bike_id: str, bike_data: dict, user_id: str) -> Optional[Bike]:
        bike_ref = self.db.collection('bikes').document(bike_id)
        bike_doc = bike_ref.get()
        
        if not bike_doc.exists:
            return None
            
        bike_data['updated_at'] = datetime.now()
        bike_ref.update(bike_data)
        
        updated_data = bike_doc.to_dict()
        updated_data.update(bike_data)
        updated_data['id'] = bike_id
        return Bike(**updated_data)

    async def delete_bike(self, bike_id: str, user_id: str) -> bool:
        bike_ref = self.db.collection('bikes').document(bike_id)
        bike_doc = bike_ref.get()
        
        if not bike_doc.exists:
            return False
            
        bike_ref.delete()
        return True

    async def get_reviews(self) -> List[Review]:
        reviews_ref = self.db.collection('reviews')
        reviews = []
        for doc in reviews_ref.stream():
            review_data = doc.to_dict()
            review_data['id'] = doc.id
            # Ensure required fields are present
            if 'user_id' not in review_data:
                review_data['user_id'] = 'test_user'  # Default user_id for testing
            if 'created_at' not in review_data:
                review_data['created_at'] = datetime.now()
            if 'updated_at' not in review_data:
                review_data['updated_at'] = datetime.now()
            reviews.append(Review(**review_data))
        return reviews

    async def get_review(self, review_id: str) -> Optional[Review]:
        review_ref = self.db.collection('reviews').document(review_id)
        review_doc = review_ref.get()
        if review_doc.exists:
            review_data = review_doc.to_dict()
            review_data['id'] = review_id
            return Review(**review_data)
        return None

    async def create_review(self, review_data: dict, user_id: str) -> Review:
        review_data['created_at'] = datetime.now()
        review_data['updated_at'] = datetime.now()
        review_data['user_id'] = user_id
        
        review_ref = self.db.collection('reviews').document()
        review_ref.set(review_data)
        
        review_data['id'] = review_ref.id
        return Review(**review_data)

    async def update_review(self, review_id: str, review_data: dict, user_id: str) -> Optional[Review]:
        review_ref = self.db.collection('reviews').document(review_id)
        review_doc = review_ref.get()
        
        if not review_doc.exists:
            return None
            
        review_data['updated_at'] = datetime.now()
        review_ref.update(review_data)
        
        updated_data = review_doc.to_dict()
        updated_data.update(review_data)
        updated_data['id'] = review_id
        return Review(**updated_data)

    async def delete_review(self, review_id: str, user_id: str) -> bool:
        review_ref = self.db.collection('reviews').document(review_id)
        review_doc = review_ref.get()
        
        if not review_doc.exists:
            return False
            
        review_ref.delete()
        return True

    async def get_brands(self) -> List[Brand]:
        brands_ref = self.db.collection('brands')
        brands = []
        for doc in brands_ref.stream():
            brand_data = doc.to_dict()
            brand_data['id'] = doc.id
            # Ensure required fields are present
            if 'created_at' not in brand_data:
                brand_data['created_at'] = datetime.now()
            if 'updated_at' not in brand_data:
                brand_data['updated_at'] = datetime.now()
            brands.append(Brand(**brand_data))
        return brands

    async def get_brand(self, brand_id: str) -> Optional[Brand]:
        brand_ref = self.db.collection('brands').document(brand_id)
        brand_doc = brand_ref.get()
        if brand_doc.exists:
            brand_data = brand_doc.to_dict()
            brand_data['id'] = brand_id
            return Brand(**brand_data)
        return None

    async def get_bike_types(self) -> List[BikeType]:
        types_ref = self.db.collection('types')
        types = []
        for doc in types_ref.stream():
            type_data = doc.to_dict()
            type_data['id'] = doc.id
            # Ensure required fields are present
            if 'created_at' not in type_data:
                type_data['created_at'] = datetime.now()
            if 'updated_at' not in type_data:
                type_data['updated_at'] = datetime.now()
            types.append(BikeType(**type_data))
        return types

    async def get_bike_type(self, type_id: str) -> Optional[BikeType]:
        type_ref = self.db.collection('types').document(type_id)
        type_doc = type_ref.get()
        if type_doc.exists:
            type_data = type_doc.to_dict()
            type_data['id'] = type_id
            return BikeType(**type_data)
        return None

    async def get_resources(self) -> List[Resource]:
        resources_ref = self.db.collection('resources')
        resources = []
        for doc in resources_ref.stream():
            resource_data = doc.to_dict()
            resource_data['id'] = doc.id
            # Ensure required fields are present
            if 'content' not in resource_data:
                resource_data['content'] = ""
            if 'created_at' not in resource_data:
                resource_data['created_at'] = datetime.now()
            if 'updated_at' not in resource_data:
                resource_data['updated_at'] = datetime.now()
            resources.append(Resource(**resource_data))
        return resources

    async def get_resource(self, resource_id: str) -> Optional[Resource]:
        resource_ref = self.db.collection('resources').document(resource_id)
        resource_doc = resource_ref.get()
        if resource_doc.exists:
            resource_data = resource_doc.to_dict()
            resource_data['id'] = resource_id
            return Resource(**resource_data)
        return None

    async def get_user(self, user_id: str) -> Optional[User]:
        user_ref = self.db.collection('users').document(user_id)
        user_doc = user_ref.get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            user_data['id'] = user_id
            return User(**user_data)
        return None

    async def create_user(self, user_data: dict) -> User:
        user_data['created_at'] = datetime.now()
        user_data['updated_at'] = datetime.now()
        
        user_ref = self.db.collection('users').document()
        user_ref.set(user_data)
        
        user_data['id'] = user_ref.id
        return User(**user_data)

    async def update_user(self, user_id: str, user_data: dict) -> Optional[User]:
        user_ref = self.db.collection('users').document(user_id)
        user_doc = user_ref.get()
        
        if not user_doc.exists:
            return None
            
        user_data['updated_at'] = datetime.now()
        user_ref.update(user_data)
        
        updated_data = user_doc.to_dict()
        updated_data.update(user_data)
        updated_data['id'] = user_id
        return User(**updated_data)

    async def delete_user(self, user_id: str) -> bool:
        user_ref = self.db.collection('users').document(user_id)
        user_doc = user_ref.get()
        
        if not user_doc.exists:
            return False
            
        user_ref.delete()
        return True

    async def get_bike_reviews(self, bike_id: str) -> List[Review]:
        reviews_ref = self.db.collection('reviews').where('bike_id', '==', bike_id)
        reviews = []
        for doc in reviews_ref.stream():
            review_data = doc.to_dict()
            review_data['id'] = doc.id
            reviews.append(Review(**review_data))
        return reviews 
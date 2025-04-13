from datetime import datetime, timedelta, UTC
from typing import Optional
import jwt
from app.models.schemas import User, UserCreate
from app.services.firebase_service import FirebaseService

class AuthService:
    def __init__(self, instance_id: str = "default"):
        self.firebase_service = FirebaseService.get_instance(instance_id)
        self.secret_key = "test_secret_key"  # For testing only
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(UTC) + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    async def register(self, user: UserCreate) -> User:
        # Check if user already exists
        existing_users = [u for u in self.firebase_service.users.values() if u.email == user.email]
        if existing_users:
            raise ValueError("Email already registered")

        # Create user
        user_data = user.model_dump()
        user_data.pop("password")  # Don't store password in plain text
        current_time = datetime.now()
        user_data["created_at"] = current_time  # Add created_at field
        user_data["updated_at"] = current_time  # Add updated_at field
        user_data["favorites"] = []  # Initialize favorites list
        created_user = await self.firebase_service.create_user(user_data)
        return created_user

    async def login(self, username: str, password: str) -> dict:
        # Find user by email (username is email in our case)
        users = [u for u in self.firebase_service.users.values() if u.email == username]
        if not users:
            raise ValueError("Invalid email or password")

        user = users[0]
        # In a real application, you would verify the password hash here
        # For testing, we'll just create a token
        access_token = self.create_access_token({"sub": user.id})
        return {"access_token": access_token, "token_type": "bearer"}

    async def get_current_user(self, token: str) -> User:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise ValueError("Could not validate credentials")
        except jwt.JWTError:
            raise ValueError("Could not validate credentials")

        user = await self.firebase_service.get_user(user_id)
        if user is None:
            raise ValueError("User not found")

        return user

    async def update_current_user(self, user_data: dict, token: str) -> User:
        current_user = await self.get_current_user(token)
        updated_user = await self.firebase_service.update_user(current_user.id, user_data)
        if not updated_user:
            raise ValueError("Could not update user")
        return updated_user

    async def logout(self, token: str) -> bool:
        # In a real application, you would invalidate the token
        # For testing, we'll just return True
        return True

    async def reset_password(self, email: str) -> bool:
        # Find user by email
        users = [u for u in self.firebase_service.users.values() if u.email == email]
        if not users:
            raise ValueError("Email not found")

        # In a real application, you would send a password reset email
        # For testing, we'll just return True
        return True 
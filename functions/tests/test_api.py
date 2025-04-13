import pytest
from fastapi.testclient import TestClient
from main import app
from app.services.firebase_service import FirebaseService
from app.models.schemas import User, Bike, Review, Brand, BikeType, Resource
from datetime import datetime
import uuid

# Test client fixture
@pytest.fixture
def client(init_firebase):
    app.state.firebase_instance_id = init_firebase
    return TestClient(app)

# Initialize Firebase service with test data
@pytest.fixture(autouse=True)
def init_firebase():
    instance_id = str(uuid.uuid4())
    firebase = FirebaseService.get_instance(instance_id)
    
    now = datetime.now()
    
    # Add test brands
    brand = Brand(
        id="brand_1",
        name="Test Brand",
        created_at=now,
        updated_at=now
    )
    firebase.brands["brand_1"] = brand

    # Add test types
    bike_type = BikeType(
        id="type_1",
        name="Test Type",
        created_at=now,
        updated_at=now
    )
    firebase.types["type_1"] = bike_type

    # Add test resources
    resource = Resource(
        id="resource_1",
        title="Test Resource",
        content="Test Content",
        type="article",
        url="http://test.com",
        created_at=now,
        updated_at=now
    )
    firebase.resources["resource_1"] = resource

    yield instance_id
    FirebaseService.clear_instance(instance_id)

# Test data
@pytest.fixture
def test_bike():
    return {
        "name": "Test Bike",
        "brand": "Test Brand",
        "model": "Test Model",
        "year": 2024,
        "type": "Test Type",
        "description": "Test Description",
        "price": 150000,
        "specs": {"test": "test"}
    }

@pytest.fixture
def test_review():
    return {
        "bike_id": "bike_1",
        "title": "Test Review",
        "content": "This is a test review",
        "rating": 4.5,
        "pros": ["Good", "Great"],
        "cons": ["None"],
        "user_id": "user_1"
    }

@pytest.fixture
def test_user():
    return {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword123",
        "role": "user"
    }

@pytest.fixture
def auth_token(client, test_user):
    # Register user
    register_response = client.post("/api/v1/auth/register", json=test_user)
    if register_response.status_code != 201:
        print(f"Registration failed: {register_response.json()}")
    assert register_response.status_code == 201
    
    # Login user
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": test_user["email"], "password": test_user["password"]}
    )
    assert login_response.status_code == 200
    return login_response.json()["access_token"]

@pytest.fixture
def test_bike_id(client, auth_token, test_bike):
    response = client.post(
        "/api/v1/bikes",
        json=test_bike,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 201
    return response.json()["id"]

@pytest.fixture
def test_review_id(client, auth_token, test_bike_id, test_review):
    test_review["bike_id"] = test_bike_id  # Update bike_id to match the created bike
    response = client.post(
        f"/api/v1/bikes/{test_bike_id}/reviews",
        json=test_review,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 201
    return response.json()["id"]

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Bangla Motorcycle Review API"}

# Bikes Tests
def test_get_bikes(client):
    response = client.get("/api/v1/bikes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_bike(client, test_bike_id):
    response = client.get(f"/api/v1/bikes/{test_bike_id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_bike_id

def test_create_bike(client, auth_token, test_bike):
    response = client.post(
        "/api/v1/bikes",
        json=test_bike,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == test_bike["name"]
    assert data["brand"] == test_bike["brand"]

def test_update_bike(client, auth_token, test_bike_id, test_bike):
    updated_bike = test_bike.copy()
    updated_bike["name"] = "Updated Test Bike"
    response = client.put(
        f"/api/v1/bikes/{test_bike_id}",
        json=updated_bike,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Test Bike"

def test_delete_bike(client, auth_token, test_bike_id):
    response = client.delete(
        f"/api/v1/bikes/{test_bike_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 204

# Reviews Tests
def test_get_reviews(client):
    response = client.get("/api/v1/reviews")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_review(client, test_bike_id, test_review_id):
    response = client.get(f"/api/v1/bikes/{test_bike_id}/reviews/{test_review_id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_review_id

def test_create_review(client, auth_token, test_bike_id, test_review):
    test_review["bike_id"] = test_bike_id  # Update bike_id to match the created bike
    response = client.post(
        f"/api/v1/bikes/{test_bike_id}/reviews",
        json=test_review,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == test_review["title"]

def test_get_bike_reviews(client, test_bike_id, test_review_id):
    response = client.get(f"/api/v1/bikes/{test_bike_id}/reviews")
    assert response.status_code == 200
    reviews = response.json()
    assert isinstance(reviews, list)
    assert len(reviews) > 0
    assert reviews[0]["id"] == test_review_id

def test_get_user_reviews(client, auth_token, test_review_id):
    response = client.get(
        "/api/v1/reviews/user/me",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    reviews = response.json()
    assert isinstance(reviews, list)
    assert len(reviews) > 0
    assert reviews[0]["id"] == test_review_id

# Other Endpoints Tests
def test_get_brands(client):
    response = client.get("/api/v1/brands")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_types(client):
    response = client.get("/api/v1/types")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_resources(client):
    response = client.get("/api/v1/resources")
    assert response.status_code == 200
    assert isinstance(response.json(), list) 
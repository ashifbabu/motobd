import pytest
from firebase_admin import firestore
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_reviews():
    response = client.get("/api/v1/reviews/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_review(test_bike, test_review):
    # First create a bike
    bike_response = client.post("/api/v1/bikes/", json=test_bike)
    bike_id = bike_response.json()["id"]
    
    # Then create a review for that bike
    review_data = test_review.copy()
    review_data["bike_id"] = bike_id
    response = client.post("/api/v1/reviews/", json=review_data)
    assert response.status_code == 201  # Changed to 201 Created
    data = response.json()
    assert data["bike_id"] == bike_id
    assert data["title"] == review_data["title"]
    assert data["content"] == review_data["content"]
    assert data["rating"] == review_data["rating"]
    assert data["pros"] == review_data["pros"]
    assert data["cons"] == review_data["cons"]
    assert "user_id" in data  # Just check if user_id exists

def test_get_review(test_bike, test_review):
    # First create a bike
    bike_response = client.post("/api/v1/bikes/", json=test_bike)
    bike_id = bike_response.json()["id"]
    
    # Then create a review
    review_data = test_review.copy()
    review_data["bike_id"] = bike_id
    create_response = client.post("/api/v1/reviews/", json=review_data)
    review_id = create_response.json()["id"]
    
    # Then get it
    response = client.get(f"/api/v1/reviews/{review_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["bike_id"] == bike_id
    assert data["title"] == review_data["title"]
    assert data["content"] == review_data["content"]
    assert data["rating"] == review_data["rating"]
    assert data["pros"] == review_data["pros"]
    assert data["cons"] == review_data["cons"]
    assert "user_id" in data  # Just check if user_id exists

def test_get_nonexistent_review(client):
    response = client.get("/api/v1/reviews/nonexistent_id")
    assert response.status_code == 404

def test_create_review_invalid_data(client):
    invalid_data = {
        "title": "Test Review",
        # Missing required fields
    }
    response = client.post("/api/v1/reviews/", json=invalid_data)
    assert response.status_code == 422  # Validation error

def test_update_review(test_bike, test_review):
    # First create a bike
    bike_response = client.post("/api/v1/bikes/", json=test_bike)
    bike_id = bike_response.json()["id"]
    
    # Then create a review
    review_data = test_review.copy()
    review_data["bike_id"] = bike_id
    create_response = client.post("/api/v1/reviews/", json=review_data)
    review_id = create_response.json()["id"]
    
    # Then update it
    updated_data = review_data.copy()
    updated_data["title"] = "Updated Review"
    response = client.put(f"/api/v1/reviews/{review_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Review"

def test_delete_review(test_bike, test_review):
    # First create a bike
    bike_response = client.post("/api/v1/bikes/", json=test_bike)
    bike_id = bike_response.json()["id"]
    
    # Then create a review
    review_data = test_review.copy()
    review_data["bike_id"] = bike_id
    create_response = client.post("/api/v1/reviews/", json=review_data)
    review_id = create_response.json()["id"]
    
    # Then delete it
    response = client.delete(f"/api/v1/reviews/{review_id}")
    assert response.status_code == 204  # Changed to 204 No Content
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/reviews/{review_id}")
    assert get_response.status_code == 404 
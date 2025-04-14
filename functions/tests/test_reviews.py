import pytest
from firebase_admin import firestore
from fastapi.testclient import TestClient

def test_get_reviews(client, db):
    response = client.get("/api/v1/reviews/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_review(client, db, test_review_data, test_bike_data):
    # First create a bike
    bike_ref = db.collection("bikes").document()
    bike_ref.set(test_bike_data)
    bike_id = bike_ref.id
    
    # Update review data with the bike ID
    test_review_data["bike_id"] = bike_id
    
    response = client.post("/api/v1/reviews/", json=test_review_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_review_data["title"]
    assert data["bike_id"] == bike_id
    
    # Clean up
    review_id = data["id"]
    db.collection("reviews").document(review_id).delete()
    db.collection("bikes").document(bike_id).delete()

def test_get_review(client, db, test_review_data, test_bike_data):
    # Create a bike first
    bike_ref = db.collection("bikes").document()
    bike_ref.set(test_bike_data)
    bike_id = bike_ref.id
    
    # Create a review
    test_review_data["bike_id"] = bike_id
    review_ref = db.collection("reviews").document()
    review_ref.set(test_review_data)
    review_id = review_ref.id

    response = client.get(f"/api/v1/reviews/{review_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_review_data["title"]
    
    # Clean up
    db.collection("reviews").document(review_id).delete()
    db.collection("bikes").document(bike_id).delete()

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

def test_update_review(client, db, test_review_data, test_bike_data):
    # Create a bike first
    bike_ref = db.collection("bikes").document()
    bike_ref.set(test_bike_data)
    bike_id = bike_ref.id
    
    # Create a review
    test_review_data["bike_id"] = bike_id
    review_ref = db.collection("reviews").document()
    review_ref.set(test_review_data)
    review_id = review_ref.id

    # Update the review
    updated_data = test_review_data.copy()
    updated_data["title"] = "Updated Review Title"
    
    response = client.put(f"/api/v1/reviews/{review_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Review Title"
    
    # Clean up
    db.collection("reviews").document(review_id).delete()
    db.collection("bikes").document(bike_id).delete()

def test_delete_review(client, db, test_review_data, test_bike_data):
    # Create a bike first
    bike_ref = db.collection("bikes").document()
    bike_ref.set(test_bike_data)
    bike_id = bike_ref.id
    
    # Create a review
    test_review_data["bike_id"] = bike_id
    review_ref = db.collection("reviews").document()
    review_ref.set(test_review_data)
    review_id = review_ref.id

    response = client.delete(f"/api/v1/reviews/{review_id}")
    assert response.status_code == 200
    
    # Verify the review is deleted
    deleted_review = db.collection("reviews").document(review_id).get()
    assert not deleted_review.exists
    
    # Clean up
    db.collection("bikes").document(bike_id).delete() 
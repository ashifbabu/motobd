import pytest
from firebase_admin import firestore

def test_get_bikes(client, db):
    response = client.get("/bikes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_bike(client, db, test_bike_data):
    response = client.post("/bikes/", json=test_bike_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_bike_data["name"]
    assert data["brand"] == test_bike_data["brand"]
    
    # Clean up
    bike_id = data["id"]
    db.collection("bikes").document(bike_id).delete()

def test_get_bike(client, db, test_bike_data):
    # Create a test bike first
    bike_ref = db.collection("bikes").document()
    bike_ref.set(test_bike_data)
    bike_id = bike_ref.id

    response = client.get(f"/bikes/{bike_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_bike_data["name"]
    
    # Clean up
    db.collection("bikes").document(bike_id).delete()

def test_get_nonexistent_bike(client):
    response = client.get("/bikes/nonexistent_id")
    assert response.status_code == 404

def test_create_bike_invalid_data(client):
    invalid_data = {
        "name": "Test Bike",
        # Missing required fields
    }
    response = client.post("/bikes/", json=invalid_data)
    assert response.status_code == 422  # Validation error 

def test_update_bike(client, db, test_bike_data):
    # Create a test bike first
    bike_ref = db.collection("bikes").document()
    bike_ref.set(test_bike_data)
    bike_id = bike_ref.id

    # Update the bike
    updated_data = test_bike_data.copy()
    updated_data["name"] = "Updated Bike Name"
    
    response = client.put(f"/bikes/{bike_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Bike Name"
    
    # Clean up
    db.collection("bikes").document(bike_id).delete()

def test_delete_bike(client, db, test_bike_data):
    # Create a test bike first
    bike_ref = db.collection("bikes").document()
    bike_ref.set(test_bike_data)
    bike_id = bike_ref.id

    response = client.delete(f"/bikes/{bike_id}")
    assert response.status_code == 200
    
    # Verify the bike is deleted
    deleted_bike = db.collection("bikes").document(bike_id).get()
    assert not deleted_bike.exists

def test_search_bikes(client, db, test_bike_data):
    # Create a test bike first
    bike_ref = db.collection("bikes").document()
    bike_ref.set(test_bike_data)
    bike_id = bike_ref.id

    response = client.get("/bikes/search?q=Test")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    
    # Clean up
    db.collection("bikes").document(bike_id).delete()

def test_filter_bikes(client, db, test_bike_data):
    # Create a test bike first
    bike_ref = db.collection("bikes").document()
    bike_ref.set(test_bike_data)
    bike_id = bike_ref.id

    response = client.get("/bikes/filter?brand=Test%20Brand")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    
    # Clean up
    db.collection("bikes").document(bike_id).delete() 
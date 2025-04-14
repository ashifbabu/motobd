import pytest
from firebase_admin import firestore
from fastapi.testclient import TestClient

@pytest.fixture
def test_type_data():
    return {
        "name": "Sports",
        "description": "High-performance motorcycles",
        "characteristics": ["High speed", "Agile handling", "Sporty design"],
        "image": "sports_bike.jpg"
    }

def test_get_types(client, db):
    response = client.get("/api/v1/types/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_type(client, db, test_type_data):
    response = client.post("/api/v1/types/", json=test_type_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_type_data["name"]
    
    # Clean up
    type_id = data["id"]
    db.collection("types").document(type_id).delete()

def test_get_type(client, db, test_type_data):
    # Create a test type first
    type_ref = db.collection("types").document()
    type_ref.set(test_type_data)
    type_id = type_ref.id

    response = client.get(f"/api/v1/types/{type_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_type_data["name"]
    
    # Clean up
    db.collection("types").document(type_id).delete()

def test_update_type(client, db, test_type_data):
    # Create a test type first
    type_ref = db.collection("types").document()
    type_ref.set(test_type_data)
    type_id = type_ref.id

    # Update the type
    updated_data = test_type_data.copy()
    updated_data["name"] = "Updated Type Name"
    
    response = client.put(f"/api/v1/types/{type_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Type Name"
    
    # Clean up
    db.collection("types").document(type_id).delete()

def test_delete_type(client, db, test_type_data):
    # Create a test type first
    type_ref = db.collection("types").document()
    type_ref.set(test_type_data)
    type_id = type_ref.id

    response = client.delete(f"/api/v1/types/{type_id}")
    assert response.status_code == 200
    
    # Verify the type is deleted
    deleted_type = db.collection("types").document(type_id).get()
    assert not deleted_type.exists 
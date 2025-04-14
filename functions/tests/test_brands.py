import pytest
from firebase_admin import firestore
from fastapi.testclient import TestClient

@pytest.fixture
def test_brand_data():
    return {
        "name": "Test Brand",
        "description": "A test motorcycle brand",
        "country": "Test Country",
        "founded_year": 2000,
        "website": "https://testbrand.com",
        "logo": "test_logo.jpg"
    }

def test_get_brands(client, db):
    response = client.get("/api/v1/brands/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_brand(client, db, test_brand_data):
    response = client.post("/api/v1/brands/", json=test_brand_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_brand_data["name"]
    
    # Clean up
    brand_id = data["id"]
    db.collection("brands").document(brand_id).delete()

def test_get_brand(client, db, test_brand_data):
    # Create a test brand first
    brand_ref = db.collection("brands").document()
    brand_ref.set(test_brand_data)
    brand_id = brand_ref.id

    response = client.get(f"/api/v1/brands/{brand_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_brand_data["name"]
    
    # Clean up
    db.collection("brands").document(brand_id).delete()

def test_update_brand(client, db, test_brand_data):
    # Create a test brand first
    brand_ref = db.collection("brands").document()
    brand_ref.set(test_brand_data)
    brand_id = brand_ref.id

    # Update the brand
    updated_data = test_brand_data.copy()
    updated_data["name"] = "Updated Brand Name"
    
    response = client.put(f"/api/v1/brands/{brand_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Brand Name"
    
    # Clean up
    db.collection("brands").document(brand_id).delete()

def test_delete_brand(client, db, test_brand_data):
    # Create a test brand first
    brand_ref = db.collection("brands").document()
    brand_ref.set(test_brand_data)
    brand_id = brand_ref.id

    response = client.delete(f"/api/v1/brands/{brand_id}")
    assert response.status_code == 200
    
    # Verify the brand is deleted
    deleted_brand = db.collection("brands").document(brand_id).get()
    assert not deleted_brand.exists 
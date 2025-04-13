import pytest
from firebase_admin import firestore

@pytest.fixture
def test_resource_data():
    return {
        "title": "Test Resource",
        "description": "A test resource for motorcycle information",
        "type": "article",
        "url": "https://testresource.com",
        "tags": ["motorcycle", "test", "resource"],
        "author": "Test Author"
    }

def test_get_resources(client, db):
    response = client.get("/resources/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_resource(client, db, test_resource_data):
    response = client.post("/resources/", json=test_resource_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_resource_data["title"]
    
    # Clean up
    resource_id = data["id"]
    db.collection("resources").document(resource_id).delete()

def test_get_resource(client, db, test_resource_data):
    # Create a test resource first
    resource_ref = db.collection("resources").document()
    resource_ref.set(test_resource_data)
    resource_id = resource_ref.id

    response = client.get(f"/resources/{resource_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_resource_data["title"]
    
    # Clean up
    db.collection("resources").document(resource_id).delete()

def test_update_resource(client, db, test_resource_data):
    # Create a test resource first
    resource_ref = db.collection("resources").document()
    resource_ref.set(test_resource_data)
    resource_id = resource_ref.id

    # Update the resource
    updated_data = test_resource_data.copy()
    updated_data["title"] = "Updated Resource Title"
    
    response = client.put(f"/resources/{resource_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Resource Title"
    
    # Clean up
    db.collection("resources").document(resource_id).delete()

def test_delete_resource(client, db, test_resource_data):
    # Create a test resource first
    resource_ref = db.collection("resources").document()
    resource_ref.set(test_resource_data)
    resource_id = resource_ref.id

    response = client.delete(f"/resources/{resource_id}")
    assert response.status_code == 200
    
    # Verify the resource is deleted
    deleted_resource = db.collection("resources").document(resource_id).get()
    assert not deleted_resource.exists 
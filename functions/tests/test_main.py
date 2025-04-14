from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    """Test the root endpoint returns correct API information."""
    response = client.get("/")
    assert response.status_code == 200
    json_data = response.json()
    
    # Check that all required fields are present
    assert "name" in json_data
    assert "version" in json_data
    assert "environment" in json_data
    assert "status" in json_data
    
    # Check specific values
    assert json_data["name"] == "RaiderCritic API"
    assert json_data["status"] == "operational"
    assert json_data["environment"] in ["development", "production"]

def test_health():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"} 
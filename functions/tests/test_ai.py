import pytest
from firebase_admin import firestore

def test_generate_review_not_implemented(client):
    response = client.post("/reviews/ai/generate/review/", json={"bike_id": "test_bike_id"})
    assert response.status_code == 501
    assert response.json()["detail"] == "AI review generation not implemented yet"

def test_generate_summary_not_implemented(client):
    response = client.post("/reviews/ai/generate/summary/", json={"bike_id": "test_bike_id"})
    assert response.status_code == 501
    assert response.json()["detail"] == "AI summary generation not implemented yet"

def test_generate_comparison_not_implemented(client):
    response = client.post("/reviews/ai/generate/comparison/", json={"bike_ids": ["bike1", "bike2"]})
    assert response.status_code == 501
    assert response.json()["detail"] == "AI comparison generation not implemented yet" 
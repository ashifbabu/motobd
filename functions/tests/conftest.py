import pytest
from fastapi.testclient import TestClient
from firebase_admin import initialize_app, credentials, firestore, auth, delete_app, get_app
import os
import sys
import json
from dotenv import load_dotenv

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from app.services.firebase_service import FirebaseService
from app.services.auth_service import AuthService

# Load test environment variables
load_dotenv()

def pytest_sessionstart(session):
    """Initialize Firebase at the start of testing session."""
    try:
        # Try to get existing app
        firebase_app = get_app()
        delete_app(firebase_app)
    except ValueError:
        pass

    try:
        # Try to initialize with service account file
        service_account_path = os.path.join(os.path.dirname(__file__), 'firebase-service-account.json')
        if os.path.exists(service_account_path):
            cred = credentials.Certificate(service_account_path)
        else:
            # Fallback to environment variables
            cred_dict = {
                "type": "service_account",
                "project_id": os.getenv("FIREBASE_PROJECT_ID"),
                "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
                "private_key": os.getenv("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n"),
                "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
                "client_id": os.getenv("FIREBASE_CLIENT_ID"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_CERT_URL")
            }
            cred = credentials.Certificate(cred_dict)
        
        initialize_app(cred, {
            'projectId': os.getenv('FIREBASE_PROJECT_ID')
        })
    except Exception as e:
        print(f"Warning: Could not initialize Firebase with credentials: {e}")
        print("Falling back to application default credentials")
        cred = credentials.ApplicationDefault()
        initialize_app(cred, {
            'projectId': os.getenv('FIREBASE_PROJECT_ID')
        })

def pytest_sessionfinish(session, exitstatus):
    """Clean up Firebase at the end of testing session."""
    try:
        firebase_app = get_app()
        delete_app(firebase_app)
    except ValueError:
        pass

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def db():
    return firestore.client()

@pytest.fixture
def firebase_service():
    return FirebaseService()

@pytest.fixture
def auth_service():
    return AuthService()

@pytest.fixture
def test_user():
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }

@pytest.fixture
def test_bike():
    return {
        "name": "Test Bike",
        "brand": "Test Brand",
        "model": "Test Model",
        "year": 2024,
        "type": "Sport",
        "description": "A test bike for testing purposes",
        "price": 10000,
        "specs": {
            "engine": "150cc",
            "mileage": "40kmpl",
            "power": "15bhp"
        }
    }

@pytest.fixture
def test_review():
    return {
        "bike_id": "test_bike_id",
        "user_id": "test_user_id",
        "rating": 4,
        "title": "Great bike",
        "content": "This is a test review",
        "pros": ["Good mileage", "Comfortable"],
        "cons": ["Bit expensive"]
    }

@pytest.fixture
def test_brand():
    return {
        "name": "Test Brand",
        "country": "Test Country",
        "description": "A test brand"
    }

@pytest.fixture
def test_bike_type():
    return {
        "name": "Sport",
        "description": "Sport bikes"
    }

@pytest.fixture
def test_resource():
    return {
        "title": "Test Resource",
        "description": "A test resource",
        "url": "https://example.com/resource",
        "type": "article"
    } 
import os
import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firebase():
    """Initialize Firebase Admin SDK with service account credentials."""
    try:
        # Get the path to the service account file
        cred_path = os.path.join(os.path.dirname(__file__), '../../config/serviceAccountKey.json')
        
        # Initialize with service account
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    except ValueError:
        # If already initialized, get the existing app
        return firebase_admin.get_app()
    except FileNotFoundError:
        # Fallback to application default credentials
        firebase_admin.initialize_app()
    
    return firebase_admin.get_app()

def get_firestore_client():
    """Get a Firestore client using the initialized Firebase app."""
    app = initialize_firebase()
    return firestore.client(app)

# Initialize Firebase when the module is imported
initialize_firebase() 
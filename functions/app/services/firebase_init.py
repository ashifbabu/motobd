import os
import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firebase():
    """Initialize Firebase Admin SDK with Application Default Credentials."""
    try:
        # Try to initialize with application default credentials
        firebase_admin.initialize_app()
    except ValueError:
        # If already initialized, get the existing app
        return firebase_admin.get_app()
    
    return firebase_admin.get_app()

def get_firestore_client():
    """Get a Firestore client using the initialized Firebase app."""
    app = initialize_firebase()
    return firestore.client(app)

# Initialize Firebase when the module is imported
initialize_firebase() 
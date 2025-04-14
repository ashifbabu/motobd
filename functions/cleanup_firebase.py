import firebase_admin
from firebase_admin import credentials, firestore
import os

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        # Try to initialize with service account file
        cred = credentials.Certificate('serviceAccountKey.json')
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        return None
    return firestore.client()

def delete_all_data():
    """Delete all data from all collections"""
    db = initialize_firebase()
    if not db:
        print("Failed to initialize Firebase")
        return

    # List of collections to clean (updated to include users)
    collections = ['bikes', 'brands', 'types', 'reviews', 'resources', 'users']

    for collection in collections:
        try:
            # Get all documents in the collection
            docs = db.collection(collection).get()
            
            # Delete each document
            for doc in docs:
                print(f"Deleting document {doc.id} from collection {collection}")
                doc.reference.delete()
            
            print(f"Successfully deleted all documents in collection {collection}")
        except Exception as e:
            print(f"Error deleting collection {collection}: {e}")

if __name__ == "__main__":
    print("Starting Firebase cleanup...")
    delete_all_data()
    print("Cleanup complete!") 
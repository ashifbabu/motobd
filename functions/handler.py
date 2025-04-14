import os
import sys
import json
import logging
import traceback

# Configure logging to write to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

def handle_request():
    """Handle the incoming request from Cloud Functions."""
    try:
        # Log Python environment information
        logger.info(f"Python version: {sys.version}")
        logger.info(f"Python executable: {sys.executable}")
        logger.info(f"Current working directory: {os.getcwd()}")
        logger.info(f"Directory contents: {os.listdir('.')}")
        
        # Get request information from environment variables
        method = os.environ.get('REQUEST_METHOD', 'GET')
        path = os.environ.get('PATH_INFO', '/')
        
        # Log request details and environment
        logger.info(f"Processing {method} request to {path}")
        logger.info(f"Environment variables: {dict(os.environ)}")
        
        if path == '/' or not path:
            # Handle root endpoint
            response = {
                "message": "Welcome to Bangla Motorcycle Review API",
                "version": "1.0.0",
                "status": "operational"
            }
        elif path == '/health':
            # Handle health check endpoint
            response = {"status": "healthy"}
        else:
            # Handle unknown endpoints
            response = {
                "error": "Not Found",
                "message": f"Endpoint {path} not found"
            }
        
        # Return the response
        response_json = json.dumps(response)
        logger.info(f"Sending response: {response_json}")
        print(response_json)
        return 0
        
    except Exception as e:
        # Log the full error traceback
        logger.error("Error processing request:")
        logger.error(traceback.format_exc())
        
        error_response = {
            "error": "Internal Server Error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }
        print(json.dumps(error_response))
        return 1

if __name__ == '__main__':
    try:
        exit_code = handle_request()
        logger.info(f"Handler completed with exit code: {exit_code}")
        exit(exit_code)
    except Exception as e:
        logger.error("Critical error in main:")
        logger.error(traceback.format_exc())
        exit(1) 
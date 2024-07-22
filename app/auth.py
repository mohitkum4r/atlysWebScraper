import os
from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load API key from environment variables or use a default (ensure to change this in production)
API_KEY = os.getenv("API_KEY", "somethingsomething")
API_KEY_NAME = "Authorization"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def verify_token(api_key: str = Security(api_key_header)):
    """
    Verify the provided API key against the expected API key.

    Args:
        api_key (str): The API key provided in the request header.

    Raises:
        HTTPException: If the API key is invalid.

    Returns:
        bool: True if the API key is valid, False otherwise.
    """
    if api_key == API_KEY:
        logger.info("API key verification successful")
        return True
    logger.warning("API key verification failed")
    raise HTTPException(status_code=403, detail="Invalid credentials")

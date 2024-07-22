from fastapi import APIRouter
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/readiness", response_model=dict)
def readiness_check():
    """
    Health check endpoint to verify if the application is up and running.

    Returns:
        dict: A message indicating the application status.
    """
    logger.info("Readiness check endpoint called")
    return {"message": "Application is up and running!"}

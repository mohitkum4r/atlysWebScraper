from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from app.auth import verify_token
from app.schemas import ScrapeRequestSchema
from app.scraper import Scraper
import logging

# Configure logging to display messages on the console and in a log file
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter()

def run_scraping(page_limit: int, proxy: str):
    """
    Run the scraping process with the specified page limit and proxy settings.

    Args:
        page_limit (int): The number of pages to scrape.
        proxy (str): The proxy server URL.

    Raises:
        Exception: If the scraping process encounters an error.
    """
    try:
        scraper = Scraper(page_limit=page_limit, proxy=proxy)
        scraper.scrape_website()
        logger.info("Scraping completed successfully")
    except Exception as e:
        logger.error(f"Scraping encountered an error: {e}")
        # Depending on requirements, notify or handle the error appropriately

@router.post("/scrape")
def scrape_products(background_tasks: BackgroundTasks, request: ScrapeRequestSchema, token: str = Depends(verify_token)):
    """
    Endpoint to initiate the scraping process in the background.

    Args:
        background_tasks (BackgroundTasks): FastAPI background tasks manager.
        request (ScrapeRequestSchema): Request schema containing page limit and proxy.
        token (str): API token for authentication.

    Raises:
        HTTPException: If the page limit is invalid.

    Returns:
        dict: A message indicating the scraping process has started.
    """
    # Validate the request fields
    if request.page_limit <= 0:
        raise HTTPException(status_code=400, detail="page_limit must be a positive integer")

    if request.page_limit > 10:
        raise HTTPException(status_code=400, detail="page_limit cannot exceed 10")

    # Add the scraping task to the background tasks manager
    background_tasks.add_task(run_scraping, request.page_limit, request.proxy)

    logger.info(f"Scraping started in the background with page limit {request.page_limit} and proxy {request.proxy}")
    return {"message": "Please wait while we scrape the website..."}

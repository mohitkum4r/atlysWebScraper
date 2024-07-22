from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.cache import clear_cache_products
from app.database import get_db
from app.auth import verify_token
import logging

from app.model import ProductModel

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/products", response_model=dict)
def get_products(db: Session = Depends(get_db), token: str = Depends(verify_token)):
    """
    Retrieve all products from the database.

    Args:
        db (Session): Database session dependency.
        token (str): API token for authentication.

    Returns:
        dict: A dictionary containing the status, product count, and product details.

    Raises:
        HTTPException: If there is an error retrieving products.
    """
    try:
        products = db.query(ProductModel).all()
        logger.info(f"Retrieved {len(products)} products from the database")
        return {"status": "ok", "count": len(products), "results": [product.to_dict() for product in products]}
    except Exception as e:
        logger.error(f"Error retrieving products: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/clear_cache", response_model=dict)
def clear_cache(token: str = Depends(verify_token)):
    """
    Clear all cached product images from Redis.

    Args:
        token (str): API token for authentication.

    Returns:
        dict: A message indicating the cache has been cleared.

    Raises:
        HTTPException: If there is an error clearing the cache.
    """
    try:
        clear_cache_products()
        logger.info("Cache cleared successfully")
        return {"message": "Cache cleared"}
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

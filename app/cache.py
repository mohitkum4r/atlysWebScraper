import redis
import json
from app.schemas import ProductSchema
import logging
import os

logger = logging.getLogger(__name__)

# Configure Redis client using environment variables
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

def clear_cache_products():
    """
    Clear all cached product images from the Redis cache.
    """
    try:
        keys = redis_client.keys('*')
        for key in keys:
            if key.endswith('.jpg'):
                redis_client.delete(key)
        logger.info("Cache cleared")
    except redis.RedisError as e:
        logger.error(f"Error clearing cache: {e}")

def get_all_cached_products():
    """
    Retrieve all cached products from Redis.
    """
    try:
        keys = redis_client.keys('*')
        products = []
        for key in keys:
            if key.endswith('.jpg'):
                product_data = redis_client.get(key)
                products.append(ProductSchema(**json.loads(product_data)))
        logger.info(f"Retrieved {len(products)} products from cache")
        return products
    except redis.RedisError as e:
        logger.error(f"Error retrieving cached products: {e}")
        return []

def set_products_to_cache(products):
    """
    Set a list of products to the Redis cache.
    """
    try:
        for product in products:
            cache_product(product)
    except redis.RedisError as e:
        logger.error(f"Error setting products to cache: {e}")

def cache_product(product):
    """
    Cache a single product in Redis.
    """
    try:
        image_url = product.image_url
        redis_client.set(image_url, json.dumps(product.dict()), ex=60*60*24)
        logger.info(f"Product cached: {product.title}")
    except redis.RedisError as e:
        logger.error(f"Error caching product {product.title}: {e}")

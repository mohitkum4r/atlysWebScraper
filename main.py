from fastapi import FastAPI
import logging
from app.routes import home, scraping, products
from app.database import init_db
import uvicorn
import os

# Configure logging
LOG_FORMAT = "%(levelname)s: %(asctime)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# Create a log file handler
file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(file_handler)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

# Include routers dynamically
for router in [home.router, scraping.router, products.router]:
    app.include_router(router)

if __name__ == "__main__":
    # Use environment variables for host and port configuration
    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host=host, port=port)

# Atlys Webscraper Assignment

This repository contains a FastAPI-based web scraper application that scrapes products from a given website and stores the data in a database. The application supports background tasks for scraping, caching using Redis, and API key-based authentication.

## Overview

The application includes the following features:
- Scraping product data from a website
- Storing scraped data in a database
- Caching product data in Redis
- API key-based authentication
- Readiness check endpoint

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/web-scraper-fastapi.git
    cd web-scraper-fastapi
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory and add the following content:
    ```env
    DATABASE_URL=sqlite:///./scraper.db
    API_KEY=your-secure-api-key
    REDIS_HOST=localhost
    REDIS_PORT=6379
    REDIS_DB=0
    ```

5. **Run the application**:
    ```bash
    uvicorn app.main:app --reload
    ```

## Usage

The application exposes the following endpoints:

- **Readiness Check**:
    ```http
    GET /readiness
    ```
  Checks if the application is up and running.

- **Get Products**:
    ```http
    GET /products
    ```
  Retrieves all products from the database. Requires API key authentication.

- **Start Scraping**:
    ```http
    POST /scrape
    ```
  Starts the scraping process in the background. Requires API key authentication.

- **Clear Cache**:
    ```http
    POST /clear_cache
    ```
  Clears the cached product data. Requires API key authentication.

## Sequence Diagram

![Sequence Diagram](https://static.swimlanes.io/f6c68af233fe9cc167584007365e9e1c.png)

## Postman Collection
/PostmanCollection/AtlysWebscraperCurls.postman_collection.json
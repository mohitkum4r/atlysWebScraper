import os
import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_fixed

from app.exception.ScraperException import ScraperException
from app.model import ProductModel
from app.schemas import ProductSchema
from app.database import SessionLocal
from app.cache import set_products_to_cache, get_all_cached_products
import logging

logger = logging.getLogger(__name__)

class Scraper:
    def __init__(self, page_limit=5, proxy=None):
        self.page_limit = page_limit
        self.proxy = proxy
        self.base_url = 'https://dentalstall.com/shop/'
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.proxies = {'http': proxy, 'https': proxy} if proxy else None
        self.scraped_products = []

    @retry(stop=stop_after_attempt(5), wait=wait_fixed(3))
    def fetch_page_content(self, page_number):
        url = f"{self.base_url}page/{page_number}/"
        logger.info(f"Attempting to fetch URL: {url}")
        try:
            response = requests.get(url, headers=self.headers, proxies=self.proxies)
            response.raise_for_status()
            logger.info(f"Successfully fetched page content for page {page_number}")
            return response.text
        except requests.RequestException as e:
            logger.error(f"Failed to fetch page {page_number}: {e}")
            raise ScraperException(f"Failed to fetch page {page_number}", errors=e)

    def extract_product_details(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        product_elements = soup.select('.product')
        for product in product_elements:
            try:
                title = product.find('h2').get_text().strip()
                price = product.find('span', class_='woocommerce-Price-amount').get_text().strip()
                image_url = str(product.find('img')['data-lazy-src']).strip()  # Ensure URL is a string
                image_path = self.download_image(image_url)
                self.scraped_products.append(ProductSchema(title=title, price=price, image_url=image_url, path_to_image=image_path))
                logger.info(f"Product extracted: {title}, {price}, {image_url}")
            except AttributeError as e:
                logger.warning(f"Failed to extract some product details: {e}")

    def download_image(self, image_url):
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            file_name = os.path.basename(image_url)
            file_path = os.path.join("images", file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as image_file:
                for chunk in response.iter_content(chunk_size=8192):
                    image_file.write(chunk)
            logger.info(f"Image downloaded successfully: {file_path}")
            return file_path
        except requests.RequestException as e:
            logger.error(f"Failed to download image: {image_url}, {e}")
            raise ScraperException(f"Failed to download image: {image_url}", errors=e)

    def save_products_to_database(self):
        db_session = SessionLocal()
        try:
            for product in self.scraped_products:
                existing_product = db_session.query(ProductModel).filter_by(image_url=product.image_url).first()
                if existing_product:
                    existing_product.title = product.title
                    existing_product.price = product.price
                    existing_product.path_to_image = product.path_to_image
                    logger.info(f"Updated existing product: {product.title}")
                else:
                    new_product = ProductModel(
                        title=product.title,
                        price=product.price,
                        image_url=product.image_url,
                        path_to_image=product.path_to_image
                    )
                    db_session.add(new_product)
                    logger.info(f"Added new product: {product.title}")
            db_session.commit()
            logger.info("All products have been saved to the database.")
        except Exception as e:
            db_session.rollback()
            logger.error(f"Error saving products to the database: {e}")
            raise ScraperException("Database transaction failed", errors=e)
        finally:
            db_session.close()

    def scrape_website(self):
        for page_number in range(1, self.page_limit + 1):
            try:
                html_content = self.fetch_page_content(page_number)
                self.extract_product_details(html_content)
            except ScraperException as e:
                logger.error(f"Skipping page {page_number} due to errors: {e}")
        self.save_products_to_database()
        set_products_to_cache(self.scraped_products)
        logger.info("Scraping and saving process completed successfully.")

    def load_cached_products(self):
        cached_products = get_all_cached_products()
        logger.info(f"Loaded {len(cached_products)} products from cache.")
        return cached_products

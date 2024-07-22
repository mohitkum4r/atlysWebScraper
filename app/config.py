from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    """
    Configuration settings for the application.

    Attributes:
        proxy (str): The proxy server URL for scraping. Defaults to None.
        page_limit (int): The number of pages to scrape. Defaults to 5.
    """
    proxy: str = Field(None, env="PROXY", description="The proxy server URL for scraping")
    page_limit: int = Field(5, env="PAGE_LIMIT", description="The number of pages to scrape")

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Initialize settings instance
settings = Settings()

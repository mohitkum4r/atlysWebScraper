from pydantic import BaseModel, Field

class ProductSchema(BaseModel):
    title: str = Field(..., title="Product Title", description="The title of the product")
    price: str = Field(..., title="Product Price", description="The price of the product")
    image_url: str = Field(..., title="Image URL", description="The URL of the product image")
    path_to_image: str = Field(..., title="Local Image Path", description="The local file path to the downloaded product image")

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "title": "Dental Tool Kit",
                "price": "$19.99",
                "image_url": "https://example.com/images/dental-tool-kit.jpg",
                "path_to_image": "images/dental-tool-kit.jpg"
            }
        }

class ScrapeRequestSchema(BaseModel):
    """
    Schema for scrape request containing page limit and optional proxy.
    """
    page_limit: int = Field(5, title="Page Limit", description="The number of pages to scrape", ge=1)
    proxy: str = Field(None, title="Proxy", description="Optional proxy server URL")

    class Config:
        schema_extra = {
            "example": {
                "page_limit": 5,
                "proxy": "http://proxyserver:port"
            }
        }

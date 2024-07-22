from sqlalchemy import Column, Integer, String
from .database import Base

class ProductModel(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(String)
    image_url = Column(String, unique=True)
    path_to_image = Column(String, nullable=True)

    def to_dict(self):
        """
        Convert the ProductModel instance to a dictionary.
        """
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "image_url": self.image_url,
            "path_to_image": self.path_to_image,
        }

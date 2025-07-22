from sqlalchemy import Column, Integer, String, Numeric, DateTime, Enum, func
from sqlalchemy.orm import relationship
from database import Base
import enum

class ProductType(enum.Enum):
    technology = "technology"
    clothing = "clothing"
    accessories = "accessories"
    beauty = "beauty"
    sports = "sports"

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(50), nullable=False)
    description = Column(String, nullable=False)
    price = Column(Numeric, nullable=False)
    image_url = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    product_type = Column(Enum(ProductType), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    order_items = relationship("OrderItem", back_populates="product")
    cart_items = relationship("CartItem", back_populates="product")
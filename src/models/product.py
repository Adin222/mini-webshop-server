from sqlalchemy import Column, Integer, String, Numeric, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(50), nullable=False)
    description = Column(String, nullable=False)
    price = Column(Numeric, nullable=False)
    image_url = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    cart_items = relationship("CartItem", back_populates="product")
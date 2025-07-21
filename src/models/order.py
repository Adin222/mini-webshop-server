from sqlalchemy import Column, Integer, String, Enum, DateTime, Numeric, func, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import enum

class OrderStatus(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, nullable=False)
    buyer_name = Column(String(30), nullable=False)
    buyer_lastname = Column(String(30), nullable=False)
    buyer_address = Column(String(40), nullable=False)
    buyer_phone_number = Column(String(50), nullable=True)
    buyer_email = Column(String(50), nullable=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    hash_password = Column(String, nullable=False)
    name = Column(String(50), nullable=False)
    email = Column(String(120), nullable=True)
    refresh_tokens = relationship("RefreshToken", back_populates="user")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="refresh_tokens")
    expires_at = Column(DateTime(timezone=True), nullable=False)
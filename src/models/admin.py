from sqlalchemy import Column, Integer, String
from database import Base

class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    hash_password = Column(String, nullable=False)
    name = Column(String(50), nullable=False)
    email = Column(String(120), nullable=True)

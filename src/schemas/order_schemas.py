from pydantic import BaseModel
from typing import Optional


class OrderCreation(BaseModel):
    name: str
    last_name: str
    phone: str
    address: str
    email: Optional[str] = None

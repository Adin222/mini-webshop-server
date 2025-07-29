from pydantic import BaseModel


class CartItemData(BaseModel):
    product_id: int
    quantity: int

class CartAction(BaseModel):
    id: int
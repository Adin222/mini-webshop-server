from pydantic import BaseModel
from ..models.product import ProductType

class ProductData(BaseModel) :
    product_name: str
    description: str
    price: float
    image_url: str
    quantity: int
    category: str
    sub_category: str


class ProductInfo(BaseModel):
    id: int
    product_name: str
    description: str
    price: float
    image_url: str
    quantity: int
    product_type: ProductType
    product_sub_type: str 

    model_config = {
        "from_attributes": True
    }

class ProductUpdate(BaseModel):
    product_name: str
    description: str
    price: float
    image_url: str
    quantity: int

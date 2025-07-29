from fastapi import HTTPException, status
from ..repository.product_repository import ProductRepository
from ..schemas.product_schemas import ProductData, ProductInfo, ProductUpdate
from ..models.product import Product, ProductType


class ProductService : 

    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def add_product(self, data: ProductData):
        required_fields = ["product_name", "description", "image_url", "price", "quantity", "category", "sub_category",]

        for field in required_fields:
            value = getattr(data, field, None)
            if value is None or (isinstance(value, str) and value.strip() == ""):
               raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All fields are required")
            
        if data.price <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Price cannot be less than or equal to zero")
        
        if data.quantity <= 0 :
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity cannot be less than or equal to zero")

        product_type = ProductType(data.category)

        product = Product(
            product_name=data.product_name, 
            description=data.description, 
            image_url=data.image_url, 
            price=data.price, 
            quantity=data.quantity,
            product_type=product_type,
            product_sub_type=data.sub_category)

        self.repo.save_product(product)
    
    def get_product_by_id(self, id: int) -> ProductInfo :

        if not isinstance(id, int):
            return {}
        
        product = self.repo.get_product_by_id(id)

        if product is None :
            return {}


        response_data = ProductInfo(
            id=product.id,
            product_name=product.product_name, 
            description=product.description,
            image_url=product.image_url,
            price=product.price,
            quantity=product.quantity,
            product_type=product.product_type,
            product_sub_type=product.product_sub_type
            )
        
        return response_data
    
    def get_all_products(self, product_name: str = None, min_price: float = None, max_price: float = None, quantity: int = None, sort: str = "desc"):
        if min_price is not None and min_price <= 0:
           min_price = None
    

        if max_price is not None and max_price <= 0:
           max_price = None

        if quantity is not None and quantity < 0:
           quantity = None
        
        return self.repo.get_all_products(
        product_name=product_name,
        min_price=min_price,
        max_price=max_price,
        quantity=quantity,
        sort=sort
       )
    

    def update_product_data(self, product_data: ProductUpdate, id: int):
        product = self.repo.get_product_by_id(id)

        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product is not found")

        if product_data.product_name != "" and product_data.product_name != product.product_name:
            product.product_name = product_data.product_name

        if product_data.description != "" and product_data.description != product.description:
            product.description = product_data.description

        if product_data.price > 0 and product_data.price != product.price:
            product.price = product_data.price

        if product_data.quantity > 0 and product_data.quantity != product.quantity:
            product.quantity = product_data.quantity

        if product_data.image_url != "" and product_data.image_url != product.image_url:
            product.image_url = product_data.image_url

        self.repo.save_product(product)

        return "successfully updated"
    
    
    def soft_delete_product(self, id: int):
        product = self.repo.get_product_by_id(id)

        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product is not found")
        
        product.quantity = 0

        self.repo.save_product(product)

        return "Product has been soft deleted"

        





from sqlalchemy.orm import Session
from ..models.product import Product


class ProductRepository :

    def __init__(self, db: Session):
        self.db = db

    def save_product(self, product: Product):
        self.db.add(product)
        self.db.commit()
        
    
    def get_product_by_id(self, id: int):
        product = self.db.query(Product).filter(Product.id == id).first()
        return product
    
    
    def get_all_products(self, product_name: str = None, min_price: float = None, max_price: float = None, quantity: int = None, sort: str = "desc"):
        query = self.db.query(Product)

        query = query.filter(Product.quantity > 0)

        if product_name:
         query = query.filter(Product.product_name.ilike(f"%{product_name}%"))

        if min_price is not None and min_price > 0:
         query = query.filter(Product.price >= min_price)

        if max_price is not None and max_price > 0:
         query = query.filter(Product.price <= max_price)

        if quantity is not None and quantity > 0:
         query = query.filter(Product.quantity == quantity)

        if sort == "asc":
         query = query.order_by(Product.created_at.asc())
        else:
         query = query.order_by(Product.created_at.desc())

        return query.all()


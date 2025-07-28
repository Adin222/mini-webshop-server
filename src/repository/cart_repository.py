from sqlalchemy.orm import Session
from ..models.cart import Cart, CartItem


class CartRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_cart_by_session(self, session_id: str):
        return self.db.query(Cart).filter(Cart.session_id == session_id).first()

    def create_cart(self, session_id: str):
        cart = Cart(session_id=session_id)
        self.db.add(cart)
        self.db.commit()
        self.db.refresh(cart)
        return cart

    def get_cart_item(self, cart_id: int, product_id: int):
        return self.db.query(CartItem).filter(CartItem.cart_id == cart_id, CartItem.product_id == product_id).first()

    def add_cart_item(self, cart_item: CartItem):
        self.db.add(cart_item)
        self.db.commit()
        self.db.refresh(cart_item)
        return cart_item

    def update_cart_item(self, cart_item: CartItem):
        self.db.commit()
        self.db.refresh(cart_item)
        return cart_item

from sqlalchemy.orm import Session, joinedload
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
        self.db.add(cart_item)
        self.db.commit()
    
    def get_cart_items_by_session(self, session_id: str):
        return self.db.query(Cart).options(joinedload(Cart.items).joinedload(CartItem.product)).filter_by(session_id=session_id).first()
    
    def remove_cart_item(self, cart_item: CartItem):
        self.db.delete(cart_item)
        self.db.commit()

    def get_cart_item_by_id(self, cart_item_id: id):
        return self.db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    
    def delete_cart(self, cart: Cart) :
        self.db.delete(cart)
        self.db.commit()

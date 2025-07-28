from fastapi import HTTPException, status
from ..repository.cart_repository import CartRepository
from ..repository.product_repository import ProductRepository
from ..schemas.cart_schemas import CartItemData
from ..models.cart import CartItem


class CartService:

    def __init__(self, repo: CartRepository):
        self.repo = repo

    def add_item_to_cart(self, session_id: str, cart_item_data: CartItemData):
        if session_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No session id found"
            )

        cart = self.repo.get_cart_by_session(session_id)

        if not cart:
            cart = self.repo.create_cart(session_id)

        existing_item = self.repo.get_cart_item(cart.id, cart_item_data.product_id)

        if existing_item:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product is already in the cart"
            )

        new_item = CartItem(
            cart_id=cart.id,
            product_id=cart_item_data.product_id,
            quantity=cart_item_data.quantity
        )
        return self.repo.add_cart_item(new_item)

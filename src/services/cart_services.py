from fastapi import HTTPException, status
from ..repository.cart_repository import CartRepository
from ..repository.product_repository import ProductRepository
from ..schemas.cart_schemas import CartItemData, CartAction
from ..models.cart import CartItem


class CartService:

    def __init__(self, repo: CartRepository, product_repo: ProductRepository):
        self.repo = repo
        self.product_repo = product_repo

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

    def get_cart_data(self, session_id: str):
        if session_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No session id found"
            )

        cart = self.repo.get_cart_by_session(session_id)

        if cart is None or not cart.items:
            return {
                "items": [],
                "total_price": 0
            }

        items = []
        total_price = 0

        for item in cart.items:
            product = item.product
            if product:
                item_total = item.quantity * product.price
                total_price += item_total

                items.append({
                    "id": item.id,
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "name": product.product_name,
                    "image_url": product.image_url,
                    "price": product.price
                })

        return {
            "items": items,
            "total_price": total_price
        }
    
    def remove_cart_item(self, cart_item_id: int, session_id: str):
        cart = self.repo.get_cart_by_session(session_id)

        if session_id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="session_id not found")

        if cart is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="cart not found"
            )
        
        cart_item = self.repo.get_cart_item_by_id(cart_item_id)

        if cart_item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cart item not found")
        
        cart_lazy = self.repo.get_cart_by_session(session_id)

        total_cart_items = len(cart_lazy.items)

        self.repo.remove_cart_item(cart_item)

        if total_cart_items == 1:
            self.repo.delete_cart(cart)

        return {"message": "Item removed successfully deleted."}
    
    def increase_decrease_quantity(self, cart_item_data: CartAction, action: str):
        cart_item = self.repo.get_cart_item_by_id(cart_item_data.id)

        if cart_item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cart item not found")
        
        product = self.product_repo.get_product_by_id(cart_item.product_id)

        current_quantity_in_cart = cart_item.quantity
        available_stock = product.quantity

        if action == "dec":
            if current_quantity_in_cart <= 1:
               raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot decrease below 1")
        
            cart_item.quantity -= 1
            self.repo.update_cart_item(cart_item)
            return {'message': "Quantity decreased"}
             
           
        if action == "inc":
            if current_quantity_in_cart >= available_stock:
               raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough stock available")
        
        cart_item.quantity += 1
        self.repo.update_cart_item(cart_item)
        return {'message': "Quantity increased"}

        






            


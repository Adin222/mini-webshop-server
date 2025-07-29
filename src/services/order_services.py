from fastapi import HTTPException, status
from ..repository.order_repository import OrderRepository
from ..repository.cart_repository import CartRepository
from ..repository.product_repository import ProductRepository
from ..repository.user_repository import UserRepository
from ..schemas.order_schemas import OrderCreation
from ..utils.order_util import OrderUtil
from ..models.order import Order, OrderItem, OrderStatus


class OrderService:
    def __init__(self, order_repo: OrderRepository, cart_repo: CartRepository, prod_repo: ProductRepository, user_repo: UserRepository):
        self.order_repo = order_repo
        self.cart_repo = cart_repo
        self.prod_repo = prod_repo
        self.user_repo = user_repo

    def create_order(self, session_id: str, order_data: OrderCreation):
        if session_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session ID is missing"
            )

        if not OrderUtil.valid_order_data(order_data):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data is missing"
            )

        if not OrderUtil.is_valid_phone(order_data.phone):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number must contain at least one digit"
            )

        cart = self.cart_repo.get_cart_items_by_session(session_id)

        if not cart or not cart.items:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart is empty or not found"
            )

        order = Order(
            buyer_name=order_data.name,
            buyer_lastname=order_data.last_name,
            buyer_address=order_data.address,
            buyer_phone_number=order_data.phone,
            buyer_email=order_data.email,
        )

        order.items = []

        for cart_item in cart.items:
            product = self.prod_repo.get_product_by_id(cart_item.product_id)

            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with ID {cart_item.product_id} not found"
                )

            if product.quantity < cart_item.quantity:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough stock for product")

            product.quantity -= cart_item.quantity
            self.prod_repo.save_product(product)

            order_item = OrderItem(
                product_id=product.id,
                quantity=cart_item.quantity,
            )

            order.items.append(order_item)

        user = self.user_repo.get_user_by_id(1)

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user doesn't exist")

        self.order_repo.save_order(order)
        self.cart_repo.delete_cart(cart)

        OrderUtil.send_dummy_email(user.email, order_data)

        return "Order successfully created"
    
    def get_orders_paginated(self, page: int = 1, page_size: int = 10, sort_asc: bool = True):
        query = self.order_repo.get_orders_query(sort_asc)

        total_orders = query.count()

        orders = query.offset((page - 1) * page_size).limit(page_size).all()

        results = []
        for order in orders:
            total_price = 0
            for item in order.items:
                total_price += item.quantity * float(item.product.price)
            results.append({
                "id": order.id,
                "created_at": order.created_at,
                "status": order.status.value,
                "total_price": total_price,
                "finished": order.finished
            })

        return results, total_orders
    
    def get_order_details(self, id: int):
        order = self.order_repo.get_order_by_id(id)

        if order is None:
            HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order doesn't exist")

        detailed_items = []
        order_total = 0
        for item in order.items:
            product = self.prod_repo.get_product_by_id(item.product_id)

            if product is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product doesn't exist")
            
            order_total += (product.price * item.quantity)
            detailed_items.append({
                "product_id": product.id,
                "quantity": item.quantity,
                "image": product.image_url,
                "price": product.price,
                "name": product.product_name
            })

        return {
                "order_id": order.id,
                "order_total": order_total,
                "items": detailed_items
        }
    
    def update_order_status(self, id: int, status: str):
        if status is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="status doesn't exist")

        order = self.order_repo.get_order_by_id_simple(id)

        if order is None: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order doesn't exist")
        
        if status != "accepted" and status != "rejected" and status != "finished":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid status")
        
        if status == "accepted" or status == "rejected":
            order.status = OrderStatus(status)

        if status == "finished":
            order.finished = True

        self.order_repo.save_order(order)

        return "Successfully changed status"
        





        


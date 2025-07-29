from fastapi import HTTPException, status
from ..repository.order_repository import OrderRepository
from ..repository.cart_repository import CartRepository
from ..repository.product_repository import ProductRepository
from ..repository.user_repository import UserRepository
from ..schemas.order_schemas import OrderCreation
from ..utils.order_util import OrderUtil
from ..models.order import Order, OrderItem


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
            })

        return results, total_orders

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from database import get_db
from ..repository.order_repository import OrderRepository
from ..repository.cart_repository import CartRepository
from ..repository.product_repository import ProductRepository
from ..repository.user_repository import UserRepository
from ..services.order_services import OrderService
from ..schemas.order_schemas import OrderCreation

router = APIRouter(prefix="/api", tags=["Order"])

def get_order_service(db: Session = Depends(get_db)) -> OrderService :
    repo = OrderRepository(db)
    cart_repo = CartRepository(db)
    prod_repo = ProductRepository(db)
    user_repo = UserRepository(db)
    return OrderService(repo, cart_repo, prod_repo, user_repo)


@router.post('/create-order')
def create_order(order_data: OrderCreation, request: Request, services: OrderService = Depends(get_order_service)):
    session_id = request.cookies.get('session_id')

    response = services.create_order(session_id, order_data)

    return {'order' : response}


@router.get("/orders")
def list_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    sort_asc: bool = Query(True),
    order_service: OrderService = Depends(get_order_service)
):
    orders, total = order_service.get_orders_paginated(page, page_size, sort_asc)

    return {
        "page": page,
        "page_size": page_size,
        "total_orders": total,
        "orders": orders
    }
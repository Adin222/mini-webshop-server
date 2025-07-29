from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from ..schemas.cart_schemas import CartItemData, CartAction
from database import get_db
from ..repository.cart_repository import CartRepository
from ..repository.product_repository import ProductRepository
from ..services.cart_services import CartService

router = APIRouter(prefix="/api", tags=["Cart"])

def get_auth_service(db: Session = Depends(get_db)) -> CartService :
    repo = CartRepository(db)
    product_repo = ProductRepository(db)
    return CartService(repo, product_repo) 

@router.post("/add-item")
def add_item_to_cart(request: Request, item_data: CartItemData, service: CartService = Depends(get_auth_service)):
    session_id = request.cookies.get("session_id")

    added_item = service.add_item_to_cart(session_id, item_data)
    return {"message": "Item added to cart", "item": {
        "product_id": added_item.product_id,
        "quantity": added_item.quantity
    }}

@router.get("/get-items")
def get_cart_data(request: Request, service: CartService = Depends(get_auth_service)):
    session_id = request.cookies.get("session_id")

    cart_items = service.get_cart_data(session_id)

    return cart_items

@router.delete("/remove-item/{id}")
def remove_cart_item(id: int, request: Request, service: CartService = Depends(get_auth_service)):
    session_id = request.cookies.get("session_id")

    response = service.remove_cart_item(id, session_id)

    return response

@router.patch("/cart/{action}")
def increase_decrease_quantity(action: str, cart_item: CartAction, service: CartService = Depends(get_auth_service)):
    response = service.increase_decrease_quantity(cart_item, action)

    return response

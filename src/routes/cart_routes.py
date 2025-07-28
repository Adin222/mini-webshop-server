from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from ..schemas.cart_schemas import CartItemData
from database import get_db
from ..repository.cart_repository import CartRepository
from ..services.cart_services import CartService

router = APIRouter(prefix="/api", tags=["Cart"])

def get_auth_service(db: Session = Depends(get_db)) -> CartService :
    repo = CartRepository(db)
    return CartService(repo) 

@router.post("/add-item")
def add_item_to_cart(request: Request, item_data: CartItemData, service: CartService = Depends(get_auth_service)):
    session_id = request.cookies.get("session_id")

    added_item = service.add_item_to_cart(session_id, item_data)
    return {"message": "Item added to cart", "item": {
        "product_id": added_item.product_id,
        "quantity": added_item.quantity
    }}

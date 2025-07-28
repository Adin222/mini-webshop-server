from fastapi import APIRouter

from .auth_routes import router as auth_router
from .user_routes import router as user_router
from .product_routes import router as product_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(product_router)

__all__ = ["api_router"]
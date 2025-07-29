from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from ..auth.dependencies import require_authentication
from ..schemas.product_schemas import ProductData, ProductUpdate

from database import get_db
from ..repository.product_repository import ProductRepository
from ..services.product_services import ProductService


router = APIRouter(prefix="/api", tags=["API"])

def get_product_service(db: Session = Depends(get_db)) -> ProductService :
    repo = ProductRepository(db)
    return ProductService(repo)

@router.post('/create/product')
def create_product(product_data: ProductData, service: ProductService = Depends(get_product_service), _= Depends(require_authentication)):
    service.add_product(product_data)

    return {'product': 'product successfully added'}

@router.get("/products")
def get_all_products(
    service: ProductService = Depends(get_product_service),
    name: str = Query(None),
    min_price: float = Query(None),
    max_price: float = Query(None),
    quantity: int = Query(None),
    sort: str = Query("desc", regex="^(asc|desc)$")
):
    return service.get_all_products(
        product_name=name,
        min_price=min_price,
        max_price=max_price,
        quantity=quantity,
        sort=sort
    )

@router.get('/product/{id}')
def get_product(id: int, service: ProductService = Depends(get_product_service)):
    response = service.get_product_by_id(id)

    return {'product': response}

@router.patch('/product/{id}')
def update_product(id: int, product_data: ProductUpdate, service: ProductService = Depends(get_product_service)):
    response = service.update_product_data(product_data, id)

    return response

@router.delete('/product/{id}')
def soft_delete_project(id: int, service: ProductService = Depends(get_product_service)):
    response = service.soft_delete_product(id)

    return response
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas.user_schemas import UpdateLoggedUser, RegisterUser
from ..auth.dependencies import require_authentication

from database import get_db
from ..repository.user_repository import UserRepository
from ..services.user_services import UserService

router = APIRouter(prefix="/api", tags=["API"])

def get_user_service(db: Session = Depends(get_db)) -> UserService :
    repo = UserRepository(db)
    return UserService(repo)

@router.get('/user/{id}')
def get_logged_user(id: int, service: UserService = Depends(get_user_service), _= Depends(require_authentication)):
    response = service.get_user_by_id(id)

    return {'user': response}

@router.patch('/user/{id}')
def update_user(user_update_data: UpdateLoggedUser, id: int, service: UserService = Depends(get_user_service), _= Depends(require_authentication)):
    response = service.update_user(user_update_data, id)

    return response

@router.post('/create/admin')
def create_user(user_data: RegisterUser, service: UserService = Depends(get_user_service)):
    response = service.register_admin(user_data)

    return response
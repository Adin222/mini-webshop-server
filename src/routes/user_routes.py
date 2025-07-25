from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from ..repository.user_repository import UserRepository
from ..services.user_services import UserService

router = APIRouter(prefix="/api", tags=["API"])

def get_auth_service(db: Session = Depends(get_db)) -> UserService :
    repo = UserRepository(db)
    return UserService(repo)

@router.get('user/{id}')
def get_logged_user(id: int, service: UserService = Depends(get_auth_service)):
    response = service.get_user_by_id(id)

    return {'user': response}
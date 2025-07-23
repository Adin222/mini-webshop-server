from fastapi import APIRouter, Response, Cookie, Depends
from sqlalchemy.orm import Session

from database import get_db
from settings import ENVIRONMENT
from ..repository.auth_repository import AuthRepository
from ..services.auth_services import AuthService
from ..schemas.auth_schemas import UserLogin

router = APIRouter(prefix="/api/auth", tags=["Auth"])

def get_auth_service(db: Session = Depends(get_db)) -> AuthService :
    repo = AuthRepository(db)
    return AuthService(repo) 


@router.post("/login")
def login(login_data: UserLogin, response: Response, access_token: str = Cookie(None), service: AuthService = Depends(get_auth_service)) : 
    tokens = service.login(login_data, access_token)

    response.set_cookie(
        key="access_token",
        value=tokens['access_token'],
        httponly=True,
        secure=ENVIRONMENT=="production",      
        samesite="lax",  
        max_age=600   
    )

    response.set_cookie(
        key="refresh_token",
        value=tokens['refresh_token'],
        httponly=True,
        secure=ENVIRONMENT=="production",      
        samesite="lax",  
        max_age=864000   
    )

    return {"message": "Successfully logged in"}

@router.post("/logout")
def logout(response: Response, access_token : str = Cookie(None), refresh_token : str = Cookie(None), service: AuthService = Depends(get_auth_service)):
    service.logout(access_token, refresh_token)

    response.delete_cookie('refresh_token')
    response.delete_cookie('access_token')

    return {'message': 'Successfully logged out'}


@router.get("/me")
def me(access_token : str = Cookie(None), refresh_token : str = Cookie(None), service: AuthService = Depends(get_auth_service)) :
    response = service.me(access_token, refresh_token)
    
    return {'user': response}

@router.post("/refresh")
def refresh(response: Response, access_token: str = Cookie(None), refresh_token: str = Cookie(None), service: AuthService = Depends(get_auth_service)) :

    token =  service.refresh(access_token, refresh_token)

    response.set_cookie(
        key="access_token",
        value=token['access_token'],
        httponly=True,
        secure=ENVIRONMENT=="production",      
        samesite="lax",  
        max_age=600   
    )

    return {'message': 'Successfully refreshed'}
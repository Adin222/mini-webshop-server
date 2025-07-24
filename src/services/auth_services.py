from fastapi import HTTPException, status
from ..repository.auth_repository import AuthRepository
from ..utils.auth_util import AuthUtil
from ..models.user import RefreshToken
import secrets
from datetime import datetime, timedelta, timezone
from ..schemas.auth_schemas import UserLogin, UserResponse


class AuthService :
    
    def __init__(self, repo: AuthRepository) :
        self.repo = repo 

    
    def login(self, login_data: UserLogin, access_token: str) -> dict :
        if access_token is not None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Already logged in")
        
        if login_data.username is None or login_data.password is None :
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, details="Fields cannot be empty")

        user = self.repo.get_user_by_username(login_data.username)

        if user is None or not AuthUtil.verify_hashed_password(user.hash_password, login_data.password) : 
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
        payload = {'id': user.id, 'name': user.name, 'email': user.email, 'username': user.username}

        access_token = AuthUtil.generate_access_token(payload)

        expires_at = datetime.now(timezone.utc) + timedelta(days=10)
        token = secrets.token_urlsafe(64)
        refresh_token = RefreshToken(token=token, user_id=user.id, expires_at=expires_at)

        self.repo.save_token(refresh_token)

        return {'access_token': access_token, 'refresh_token': refresh_token.token}
    

    def logout(self, access_token: str, refresh_token: str) :
        if not access_token and not refresh_token:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Already logged out")
        
        self.repo.delete_token(refresh_token)

    def me(self, access_token : str, refresh_token: str) -> UserResponse :
        if access_token is None and refresh_token is None:
            return UserResponse(id=0, name="Guest", username="guest123", email="template", is_auth=False)

        if access_token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are logged out")
        
        payload = AuthUtil.decode_access_token(access_token)

        response = UserResponse(id=payload['id'], name=payload['name'], username=payload['username'], email=payload['email'], is_auth=True)

        return response
        
    def refresh(self, access_token : str, refresh_token: str) -> str:
        if refresh_token is None :
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are logged out")

        if access_token :
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot refresh")
        
        
        token = self.repo.get_refresh_token(refresh_token)

        if token.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc) :
            self.repo.delete_token(refresh_token)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")
        
        user = self.repo.get_user_by_id(token.user_id)

        if user is None :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist")
        
        payload = {'id': user.id, 'name': user.name, 'email': user.email, 'username': user.username}

        new_access_token = AuthUtil.generate_access_token(payload)

        return {'access_token': new_access_token}


    

    

from fastapi import HTTPException, status
from ..repository.user_repository import UserRepository
from ..schemas.user_schemas import LoggedUser, UpdateLoggedUser
from ..utils.auth_util import AuthUtil
from ..utils.user_utils import UserUtil
from ..models.user import User


class UserService:

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_user_by_id(self, id: int) -> LoggedUser :
        user = self.repo.get_user_by_id(id)

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist")
        
        mapped_user = LoggedUser(name=user.name, username=user.username, email=user.email)

        return mapped_user
    
    def update_user(self, user: UpdateLoggedUser, id: int) :

        if not any([
        user.name and user.name.strip(),
        user.email and user.email.strip(),
        user.username and user.username.strip(),
        user.password and user.password.strip(),
        ]):
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")
        
        db_user = self.repo.get_user_by_id(id)

        if db_user is None :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist")

        if db_user.username == user.username :
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already in use")
        
        if db_user.email == user.email :
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already in use")

        
        if user.name and user.name.strip() :
            db_user.name = user.name
        
        if user.email and user.email.strip() :
            email_valid = UserUtil.check_user_email(user.email)
            if not email_valid : 
               raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email format")
            db_user.email = user.email
        
        if user.username and user.username.strip() :
            db_user.username = user.username
        
        if user.password and user.password.strip() :
            password_valid = UserUtil.check_user_password(user.password)

            if not password_valid :
               raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password should be 8 chars, 1 uppercase, 1 special char")
            
            hash_password = AuthUtil.hash_password(user.password)
            db_user.hash_password = hash_password

        self.repo.save_user(db_user)

        return {'message': 'user updated successfully'}



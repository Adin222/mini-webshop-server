from fastapi import HTTPException, status
from ..repository.user_repository import UserRepository
from ..schemas.user_schemas import LoggedUser


class UserService:

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_user_by_id(self, id: int) -> LoggedUser :
        user = self.repo.get_user_by_id(id)

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist")
        
        mapped_user = LoggedUser(id=user.id, name=user.name, username=user.username, email=user.email)

        return mapped_user
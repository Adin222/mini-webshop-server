from sqlalchemy.orm import Session
from ..models import User, RefreshToken

class AuthRepository :

    def __init__(self, db: Session) :
        self.db = db
    
    def get_user_by_username(self, username: str) -> User | None :
        return self.db.query(User).filter(User.username == username).first()
    
    def save_token(self, token: RefreshToken) :
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)

    def delete_token(self, token: str):
        refresh_token = (
          self.db.query(RefreshToken)
          .filter(RefreshToken.token == token)
          .first()
         )
        if refresh_token:
          self.db.delete(refresh_token)
          self.db.commit()

    def get_refresh_token(self, token : str) -> RefreshToken :
        token = self.db.query(RefreshToken).filter(RefreshToken.token == token).first()
        return token
    
    def get_user_by_id(self, id: int) -> User :
        user = self.db.query(User).filter(User.id == id).first()
        return user
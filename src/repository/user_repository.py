from sqlalchemy.orm import Session
from ..models.user import User


class UserRepository : 

    def __init__(self, db: Session):
        self.db = db
    
    def get_user_by_id(self, id: int) -> User:
        return self.db.query(User).filter(User.id == id).first()
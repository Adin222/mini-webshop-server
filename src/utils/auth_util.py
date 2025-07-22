import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from settings import JWT_SECRET_KEY


class AuthUtil : 

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret_key = JWT_SECRET_KEY
    algorithm = "HS256"
    token_expire_minutes = 10

    @classmethod
    def hash_password(cls, password: str) -> str :
        return cls.pwd_context.hash(password)
    
    @classmethod
    def verify_hashed_password(cls, hashed_password: str, password: str) -> bool :
        return cls.pwd_context.verify(password, hashed_password)
    
    @classmethod
    def generate_access_token(cls, data: dict) -> str :
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=cls.token_expire_minutes)
        to_encode.update({'exp' : expire})
        coded_jwt = jwt.encode(to_encode, cls.secret_key, cls.algorithm)
        return coded_jwt
    
    @classmethod
    def decode_access_token(cls, token: str) -> dict :
        payload = jwt.decode(token, cls.secret_key, algorithms=[cls.algorithm])
        return payload
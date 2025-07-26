from pydantic import BaseModel, ConfigDict
from typing import Optional

class LoggedUser(BaseModel) :
    name: str
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)

class UpdateLoggedUser(BaseModel) :
    name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None  
    
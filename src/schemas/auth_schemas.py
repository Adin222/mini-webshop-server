from pydantic import BaseModel, ConfigDict

class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):

    id: int
    name: str
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)
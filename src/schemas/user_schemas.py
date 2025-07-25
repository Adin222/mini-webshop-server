from pydantic import BaseModel, ConfigDict

class LoggedUser(BaseModel) :
    id: int
    name: str
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)


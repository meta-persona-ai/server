from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    id: int
    email: str
    name: str
    picture: str | None = None
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    id: int | None = None
    email: str | None = None
    name: str | None = None
    picture: str | None = None

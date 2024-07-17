from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    email: str
    name: str
    picture: str | None = None
    is_active: bool = True
    hashed_password: str | None = None

class User(BaseModel):
    id: int
    email: str
    name: str
    picture: str | None = None
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)

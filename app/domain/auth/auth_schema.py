from pydantic import BaseModel


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

    class Config:
        from_attributes = True

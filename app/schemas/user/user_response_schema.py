from pydantic import BaseModel

class User(BaseModel):
    id: int
    email: str
    name: str
    picture: str | None = None
    is_active: bool = True

    class Config:
        from_attributes = True

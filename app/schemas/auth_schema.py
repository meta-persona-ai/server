from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    user_id: int
    user_email: str
    user_name: str
    user_password: str | None = None
    user_profile: str | None = None
    user_is_active: bool = True

class User(BaseModel):
    id: int
    email: str
    name: str
    picture: str | None = None
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)

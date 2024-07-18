from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    user_id: int
    user_email: str
    user_name: str
    user_profile: str | None = None

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    user_email: str | None = None
    user_name: str | None = None
    user_profile: str | None = None

from fastapi_camelcase import CamelModel
from datetime import datetime

from app.models.user import Gender

class UserCreate(CamelModel):
    user_id: int | None = None
    user_email: str
    user_name: str
    user_password: str | None = None
    user_profile: str | None = None
    user_is_active: bool = True


class UserUpdate(CamelModel):
    # user_email: str | None = None
    user_name: str | None = None
    user_profile: str | None = None
    user_gender: Gender | None = None
    user_birthdate: datetime | None = None
from fastapi_camelcase import CamelModel
from pydantic import ConfigDict
from datetime import datetime

from app.models.user import Gender


class UserResponse(CamelModel):
    user_id: int
    user_email: str
    user_name: str
    user_profile: str | None = None
    user_gender: Gender | None = None
    user_birthdate: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class MessageResponse(CamelModel):
    message: str
from fastapi_camelcase import CamelModel
from pydantic import ConfigDict


class UserResponse(CamelModel):
    user_id: int
    user_email: str
    user_name: str
    user_profile: str | None = None

    model_config = ConfigDict(from_attributes=True)

class MessageResponse(CamelModel):
    message: str
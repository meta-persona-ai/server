from fastapi_camelcase import CamelModel
from pydantic import ConfigDict
from datetime import datetime


class ChatResponse(CamelModel):
    chat_id: int
    user_id: int
    character_id: int
    chat_create_at: datetime

    model_config = ConfigDict(from_attributes=True)

class MessageResponse(CamelModel):
    message: str
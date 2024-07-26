from fastapi_camelcase import CamelModel
from datetime import datetime
from enum import Enum


class ChatLogRoolEnum(str, Enum):
    user = 'user'
    character = 'character'

class ChatLogResponse(CamelModel):
    log_id: int
    chat_id: int
    user_id: int
    character_id: int
    role: ChatLogRoolEnum
    log_create_at: datetime

class MessageResponse(CamelModel):
    message: str
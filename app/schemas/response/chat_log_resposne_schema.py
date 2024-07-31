from fastapi_camelcase import CamelModel
from datetime import datetime
from enum import Enum

class User(CamelModel):
    user_id: int
    user_email: str
    user_name: str
    user_profile: str | None = None

class Character(CamelModel):
    character_id: int
    character_name: str
    character_profile: str | None = None

class ChatLogRoolEnum(str, Enum):
    user = 'user'
    character = 'character'

class ChatLogResponse(CamelModel):
    log_id: int
    chat_id: int
    role: ChatLogRoolEnum
    contents: str
    log_create_at: datetime

    user: User
    character: Character

class MessageResponse(CamelModel):
    message: str
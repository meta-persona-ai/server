from pydantic import BaseModel
from enum import Enum


class ChatLogRoolEnum(str, Enum):
    user = 'user'
    character = 'character'

class ChatLogCreate(BaseModel):
    chat_id: int
    user_id: int
    character_id: int
    role: ChatLogRoolEnum
    contents: str
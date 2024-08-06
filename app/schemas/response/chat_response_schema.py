from fastapi_camelcase import CamelModel
from pydantic import field_serializer
from datetime import datetime

class User(CamelModel):
    user_id: int
    user_name: str
    user_profile: str

class Character(CamelModel):
    character_id: int
    character_name: str
    character_profile: str

class ChatLogs(CamelModel):
    log_id: int
    contents: str

class ChatResponse(CamelModel):
    chat_id: int
    user_id: int
    character_id: int
    chat_create_at: datetime
    last_message_at: datetime

    chat_logs: list[ChatLogs]

    user: User
    character: Character

    @field_serializer("chat_create_at", "last_message_at")
    def serialize_datetime(self, v: datetime):
        return v.isoformat()

class ChatCreateResponse(CamelModel):
    message: str
    chat_id: int

class MessageResponse(CamelModel):
    message: str
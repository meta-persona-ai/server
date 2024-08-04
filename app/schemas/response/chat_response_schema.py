from fastapi_camelcase import CamelModel
from pydantic import ConfigDict
from datetime import datetime

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

    model_config = ConfigDict(from_attributes=True)

class ChatCreateResponse(CamelModel):
    message: str
    chat_id: int

class MessageResponse(CamelModel):
    message: str
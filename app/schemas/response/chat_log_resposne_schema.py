from fastapi_camelcase import CamelModel
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
    
    # log_create_at = Column(DATETIME(fsp=3), default=lambda: datetime.now(timezone.utc))

class MessageResponse(CamelModel):
    message: str
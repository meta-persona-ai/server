from pydantic import BaseModel, ConfigDict


class ChatCreate(BaseModel):
    chat_id: int
    user_id: str
    character_id: str

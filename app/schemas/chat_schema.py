from pydantic import BaseModel


class ChatCreate(BaseModel):
    chat_id: int | None = None
    user_id: int
    character_id: int

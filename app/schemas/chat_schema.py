from pydantic import BaseModel


class ChatCreate(BaseModel):
    chat_id: int | None = None
    user_id: int
    character_id: int

class ChatResponse(BaseModel):
    chat_id: int
    user_id: int
    character_id: int
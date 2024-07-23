from fastapi_camelcase import CamelModel


class ChatResponse(CamelModel):
    chat_id: int
    user_id: int
    character_id: int

class MessageResponse(CamelModel):
    message: str
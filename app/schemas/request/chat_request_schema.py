from fastapi_camelcase import CamelModel


class ChatCreate(CamelModel):
    chat_id: int | None = None
    user_id: int
    character_id: int
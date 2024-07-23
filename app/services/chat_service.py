from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..crud import chat_crud
from ..models.chat import Chat
from ..schemas.request.chat_request_schema import ChatCreate


# insert
def create_chat(chat: ChatCreate, db: Session):
    return chat_crud.create_chat(chat, db)

# select
def get_chats_by_user_id(user_id: int, db: Session) -> list[Chat]:
    chats = chat_crud.get_chats_by_user_id(user_id, db)
    if not chats:
        raise HTTPException(status_code=404, detail="Chats not found")
    return chats

# delete
def delete_chat_by_id(chat_id: int, user_id: int, db: Session) -> bool:
    success = chat_crud.delete_chat_by_id(chat_id, user_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Chat not found or not authorized to delete")
    return success

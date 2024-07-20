from sqlalchemy.orm import Session

from ..models.chat import Chat
from ..schemas.chat_schema import ChatCreate


# insert
def create_chat(chat: ChatCreate, db: Session):
    db_chat = Chat(
        user_id=chat.user_id,
        character_id=chat.character_id,
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

# select
def get_chats_by_user_id(user_id: int, db: Session) -> list[Chat]:
    return db.query(Chat).filter(Chat.user_id == user_id).all()

# delete
def delete_chat_by_id(chat_id: int, user_id: int, db: Session) -> bool:
    user_to_delete = db.query(Chat).filter(
        Chat.chat_id == chat_id,
        Chat.user_id == user_id
        ).first()
    if user_to_delete:
        db.delete(user_to_delete)
        db.commit()
        return True
    return False
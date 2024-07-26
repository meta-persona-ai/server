from sqlalchemy.orm import Session

from ..models.chat_log import ChatLog
from ..schemas.request.chat_log_request_schema import ChatLogCreate


# insert
def create_chat_log(log: ChatLogCreate, db: Session) -> ChatLog:
    db_log = ChatLog(
        chat_id=log.chat_id,
        user_id=log.user_id,
        character_id=log.character_id,
        rool=log.rool,
        contents=log.contents
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

# select
def get_chat_logs_by_user_id(chat_id: int, user_id: int, db: Session) -> list[ChatLog]:
    return db.query(ChatLog).filter(
        ChatLog.chat_id == chat_id, 
        ChatLog.user_id == user_id, 
        ).all()

# def get_chats_by_chat_id_and_user_id(chat_id: int, user_id: int, db: Session) -> Chat:
#     return db.query(Chat).filter(Chat.chat_id == chat_id, Chat.user_id == user_id).first()

# # delete
# def delete_chat_by_id(chat_id: int, user_id: int, db: Session) -> bool:
#     user_to_delete = db.query(Chat).filter(
#         Chat.chat_id == chat_id,
#         Chat.user_id == user_id
#         ).first()
#     if user_to_delete:
#         db.delete(user_to_delete)
#         db.commit()
#         return True
#     return False
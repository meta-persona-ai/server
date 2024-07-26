from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..models.chat_log import ChatLog
from ..schemas.request.chat_log_request_schema import ChatLogCreate


# insert
def create_chat_log(log: ChatLogCreate, db: Session) -> ChatLog:
    db_log = ChatLog(
        chat_id=log.chat_id,
        user_id=log.user_id,
        character_id=log.character_id,
        role=log.role,
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
        ).order_by(ChatLog.log_create_at.desc()).all()

# delete
def delete_chat_log_by_id(log_id: int, user_id: int, db: Session) -> bool:
    log_to_delete = db.query(ChatLog).filter(
        ChatLog.log_id == log_id,
        ChatLog.user_id == user_id
        ).first()
    if log_to_delete:
        db.delete(log_to_delete)
        db.commit()
        return True
    return False
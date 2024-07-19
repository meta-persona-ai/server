from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from ..models.chat import Chat
from ..models.chat_log import ChatLog
from ..schemas.chat_schema import ChatCreate


def create_chat(chat: ChatCreate, db: Session):
    db_chat = Chat(
        user_id=chat.user_id,
        character_id=chat.character_id,
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def get_chats_by_id(user_id: int, db: Session):
    # 사용자의 채팅방을 조회
    chats = db.query(Chat).filter(Chat.user_id == user_id).all()

    # 각 채팅방의 마지막 로그를 가져오기 위한 하위 쿼리 작성
    subquery = db.query(
        ChatLog.chat_id,
        func.max(ChatLog.log_create_at).label("last_log_time")
    ).group_by(ChatLog.chat_id).subquery()

    # 채팅방과 마지막 로그를 함께 가져오기
    chat_logs = db.query(Chat, ChatLog).join(
        subquery, Chat.chat_id == subquery.c.chat_id
    ).join(
        ChatLog, (ChatLog.chat_id == Chat.chat_id) & (ChatLog.log_create_at == subquery.c.last_log_time)
    ).filter(Chat.user_id == user_id).all()

    # 결과를 보기 좋게 정리
    result = []
    for chat, chat_log in chat_logs:
        result.append({
            "chat": chat,
            "last_log": chat_log
        })

    return result

# def get_user_by_email(email: str, db: Session) -> User:
#     return db.query(User).filter(User.email == email).first()

# # update
# def update_user_by_id(user_id: int, user_data: UserUpdate, db: Session) -> User:
#     user_to_update = db.query(User).filter(User.id == user_id).first()
#     if user_to_update:
#         for attr, value in vars(user_data).items():
#             if value is not None and attr != "_sa_instance_state":
#                 setattr(user_to_update, attr, value)
#         db.commit()
#         return user_to_update
#     return None

# # delete
# def delete_user_by_id(user_id: int, db: Session) -> bool:
#     user_to_delete = db.query(User).filter(User.id == user_id).first()
#     if user_to_delete:
#         db.delete(user_to_delete)
#         db.commit()
#         return True
#     return False

# # deactivate
# def deactivate_user_by_id(user_id: int, db: Session) -> bool:
#     user_to_deactivate = db.query(User).filter(User.id == user_id).first()
#     if user_to_deactivate:
#         user_to_deactivate.is_active = False
#         db.commit()
#         return user_to_deactivate
#     return None
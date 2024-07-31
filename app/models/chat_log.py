from sqlalchemy import Column, Integer, Enum, Text, ForeignKey, BigInteger, Sequence, event, text
from datetime import datetime
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from ..db.database import Base


class ChatTypeEnum(PyEnum):
    user = 'user'
    character = 'character'

class ChatLog(Base):
    __tablename__ = "chat_logs"

    log_id = Column(BigInteger, Sequence('log_id_seq'), primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey('chats.chat_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)
    character_id = Column(BigInteger, ForeignKey('characters.character_id'), nullable=True)
    role = Column(Enum(ChatTypeEnum), nullable=False)
    log_create_at = Column(DATETIME(fsp=3), default=datetime.now, nullable=False)
    contents = Column(Text, nullable=True)

    chat = relationship("Chat", back_populates="chat_logs")
    user = relationship("User", back_populates="chat_logs")
    character = relationship("Character", back_populates="chat_logs")

@event.listens_for(ChatLog, 'before_update')
def receive_before_update(mapper, connection, target):
    target.updated_at = datetime.now()

@event.listens_for(ChatLog, 'after_insert')
def after_insert_chat_log_listener(mapper, connection, target):
    connection.execute(
        text("UPDATE chats SET last_message_at = :log_create_at WHERE chat_id = :chat_id"),
        {"log_create_at": target.log_create_at, "chat_id": target.chat_id}
    )
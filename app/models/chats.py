from sqlalchemy import Column, Integer, ForeignKey, BigInteger, event, text
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import DATETIME

from ..db import Base

class Chat(Base):
    __tablename__ = "chats"

    chat_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    character_id = Column(BigInteger, ForeignKey('characters.character_id'), nullable=False)
    chat_create_at = Column(DATETIME(fsp=3), default=datetime.now, nullable=False)
    last_message_at = Column(DATETIME(fsp=3), default=datetime.now, nullable=False)

    user = relationship("User", back_populates="chats", lazy='selectin')
    character = relationship("Character", back_populates="chats", lazy='selectin')
    chat_logs = relationship("ChatLog", back_populates="chat", lazy='selectin', cascade="all, delete-orphan")

@event.listens_for(Chat, 'after_insert')
def after_insert_listener(mapper, connection, target):
    connection.execute(
        text("UPDATE characters SET character_usage_count = character_usage_count + 1 WHERE character_id = :character_id"),
        {"character_id": target.character_id}
    )
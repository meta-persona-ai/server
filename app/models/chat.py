from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

from ..database import Base

class Chat(Base):
    __tablename__ = "chats"

    chat_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    character_id = Column(Integer, ForeignKey('characters.character_id'), nullable=False)
    chat_create_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="chats", lazy='selectin')
    character = relationship("Character", back_populates="chats", lazy='selectin')
    chat_logs = relationship("ChatLog", back_populates="chat", lazy='selectin')

# 지연 임포트
from .user import User
from .character import Character
from .chat_log import ChatLog
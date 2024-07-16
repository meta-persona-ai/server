from sqlalchemy import Column, Integer, String, DateTime, Enum, Text, ForeignKey
from datetime import datetime
from sqlalchemy.dialects.mysql import VARCHAR
from database import Base
from sqlalchemy.orm import relationship
import enum

class ChatTypeEnum(enum.Enum):
    user = 'user'
    character = 'character'

class ChatLog(Base):
    __tablename__ = "chat_logs"

    log_id = Column(VARCHAR(255), primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.chat_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)
    character_id = Column(Integer, ForeignKey('characters.character_id'), nullable=True)
    type = Column(Enum(ChatTypeEnum), nullable=False)
    log_create_at = Column(DateTime, default=datetime.now)
    contents = Column(Text, nullable=True)

    chat = relationship("Chat", back_populates="chat_logs")
    user = relationship("User", back_populates="chat_logs")
    character = relationship("Character", back_populates="chat_logs")

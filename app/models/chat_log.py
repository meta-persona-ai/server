from sqlalchemy import Column, Integer, DateTime, Enum, Text, ForeignKey, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from ..db.database import Base


class ChatTypeEnum(enum.Enum):
    user = 'user'
    character = 'character'

class ChatLog(Base):
    __tablename__ = "chat_logs"

    log_id = Column(BigInteger, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.chat_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)
    character_id = Column(Integer, ForeignKey('characters.character_id'), nullable=True)
    rool = Column(Enum(ChatTypeEnum), nullable=False)
    log_create_at = Column(DateTime(timezone=True), server_default=func.now())
    contents = Column(Text, nullable=True)

    chat = relationship("Chat", back_populates="chat_logs")
    user = relationship("User", back_populates="chat_logs")
    character = relationship("Character", back_populates="chat_logs")

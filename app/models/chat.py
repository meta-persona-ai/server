from sqlalchemy import Column, Integer, DateTime, ForeignKey, BigInteger
from datetime import datetime
from sqlalchemy.orm import relationship

from ..db.database import Base

class Chat(Base):
    __tablename__ = "chats"

    chat_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    character_id = Column(BigInteger, ForeignKey('characters.character_id'), nullable=False)
    chat_create_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="chats", lazy='selectin')
    character = relationship("Character", back_populates="chats", lazy='selectin')
    chat_logs = relationship("ChatLog", back_populates="chat", lazy='selectin', cascade="all, delete-orphan")

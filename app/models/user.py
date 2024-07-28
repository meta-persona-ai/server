from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from ..db.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String(255), unique=True)
    user_password = Column(String(255))
    user_name = Column(String(255))
    user_profile = Column(String(255))
    user_join_date = Column(DateTime, default=datetime.now)
    user_is_active = Column(Boolean, default=True)

    chats = relationship("Chat", back_populates="user")
    chat_logs = relationship("ChatLog", back_populates="user")
    characters = relationship("Character", back_populates="user")

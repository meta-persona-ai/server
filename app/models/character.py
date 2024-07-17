from sqlalchemy import Column, Integer, String, Enum, Text
from sqlalchemy.orm import relationship

from ..database import Base

class Character(Base):
    __tablename__ = "characters"

    character_id = Column(Integer, primary_key=True, autoincrement=True)
    character_name = Column(String(255), nullable=False)
    character_profile = Column(String(255), nullable=True)
    character_gender = Column(Enum('male', 'female', 'other'), nullable=True)
    character_personality = Column(String(255), nullable=True)
    character_details = Column(Text, nullable=True)

    chats = relationship("Chat", back_populates="character")
    chat_logs = relationship("ChatLog", back_populates="character")

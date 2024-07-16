from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class Character(Base):
    __tablename__ = "characters"

    character_id = Column(Integer, primary_key=True, autoincrement=True)
    character_name = Column(String(255), nullable=False)

    chats = relationship("Chat", back_populates="character")
    chat_logs = relationship("ChatLog", back_populates="character")

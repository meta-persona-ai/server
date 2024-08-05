from sqlalchemy import Column, Integer, String, BigInteger, Enum, Text, ForeignKey, Boolean, event
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.dialects.mysql import DATETIME

from ..db.database import Base
from .enums import CharacterGenderEnum

class Character(Base):
    __tablename__ = "characters"

    character_id = Column(BigInteger, primary_key=True, autoincrement=True)
    character_name = Column(String(255), nullable=False)
    character_profile = Column(String(255), nullable=True)
    character_gender = Column(Enum(CharacterGenderEnum), nullable=True)
    character_personality = Column(String(255), nullable=True)
    character_details = Column(Text, nullable=True)
    character_description = Column(String(255), nullable=True)
    character_greeting = Column(Text, nullable=True)

    character_created_at = Column(DATETIME(fsp=3), default=datetime.now, nullable=False)
    character_updated_at = Column(DATETIME(fsp=3), default=datetime.now, onupdate=datetime.now, nullable=False)

    character_is_public = Column(Boolean, default=True, nullable=False)
    character_likes = Column(Integer, default=0, nullable=False)
    character_usage_count = Column(Integer, default=0, nullable=False)
    character_is_active = Column(Boolean, default=True, nullable=False)

    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)

    user = relationship("User", back_populates="characters")
    chats = relationship("Chat", back_populates="character")
    chat_logs = relationship("ChatLog", back_populates="character")
    character_relationships = relationship("CharacterRelationship", back_populates="character", cascade="all, delete-orphan")

    @classmethod
    def is_active(cls):
        return cls.character_is_active == True


@event.listens_for(Character, 'before_update')
def receive_before_update(mapper, connection, target):
    target.character_updated_at = datetime.now()


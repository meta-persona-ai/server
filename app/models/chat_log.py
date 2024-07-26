from sqlalchemy import Column, Integer, Enum, Text, ForeignKey, BigInteger, Sequence
from datetime import datetime, timezone
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import relationship
import enum

from ..db.database import Base


class ChatTypeEnum(enum.Enum):
    user = 'user'
    character = 'character'

class ChatLog(Base):
    __tablename__ = "chat_logs"

    log_id = Column(BigInteger, Sequence('log_id_seq'), primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey('chats.chat_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)
    character_id = Column(Integer, ForeignKey('characters.character_id'), nullable=True)
    role = Column(Enum(ChatTypeEnum), nullable=False)
    log_create_at = Column(DATETIME(fsp=3), default=lambda: datetime.now(timezone.utc))
    contents = Column(Text, nullable=True)

    chat = relationship("Chat", back_populates="chat_logs")
    user = relationship("User", back_populates="chat_logs")
    character = relationship("Character", back_populates="chat_logs")

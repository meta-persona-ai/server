from sqlalchemy import Boolean, Column, Integer, String, DateTime
from datetime import datetime

from database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'persona'}

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    hashed_password = Column(String(255))
    name = Column(String(255))
    picture = Column(String(255))
    created_at = Column(DateTime, default=datetime.now())
    is_active = Column(Boolean, default=True)
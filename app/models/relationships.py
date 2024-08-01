from sqlalchemy import Column, Integer, String

from ..db.database import Base

class Relationship(Base):
    __tablename__ = "relationships"

    relationship_id = Column(Integer, primary_key=True, autoincrement=True)
    relationship_name = Column(String(255), nullable=False)
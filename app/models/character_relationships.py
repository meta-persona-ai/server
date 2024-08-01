from sqlalchemy import Column, Integer, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from ..db.database import Base

class CharacterRelationship(Base):
    __tablename__ = "character_relationships"

    id = Column(Integer, primary_key=True, autoincrement=True)
    character_id = Column(BigInteger, ForeignKey('characters.character_id'), nullable=False)
    relationship_id = Column(Integer, ForeignKey('relationships.relationship_id'), nullable=False)

    character = relationship("Character", back_populates="character_relationships")
    relationship = relationship("Relationship")

from sqlalchemy import Column, Integer, String

from ..db.database import Base

class Relationship(Base):
    __tablename__ = "default_images"

    image_id = Column(Integer, primary_key=True, autoincrement=True)
    image_name = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=False)
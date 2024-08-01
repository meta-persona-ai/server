from pydantic import BaseModel, ConfigDict
from enum import Enum
from datetime import datetime

class GenderEnum(str, Enum):
    male = 'male'
    female = 'female'
    other = 'other'

class Relationship(BaseModel):
    relationship_id: int
    relationship_name: str

    model_config = ConfigDict(from_attributes=True)

class CharacterRelationship(BaseModel):
    relationship: Relationship

    model_config = ConfigDict(from_attributes=True)

class CharacterSchema(BaseModel):
    character_id: int | None = None
    character_name: str | None = None
    character_profile: str | None = None
    character_gender: str | None = None
    character_personality: str | None = None
    character_details: str | None = None
    user_id: int | None = None

    character_relationships: list[CharacterRelationship]

    model_config = ConfigDict(from_attributes=True)

class UserSchema(BaseModel):
    user_id: int | None = None
    user_email: str | None = None
    user_name: str | None = None
    user_profile: str | None = None
    user_gender: str | None = None
    user_birthdate: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class ChatLogSchema(BaseModel):
    log_id: int
    role: str
    contents: str

    model_config = ConfigDict(from_attributes=True)
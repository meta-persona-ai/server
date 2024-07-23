from pydantic import BaseModel
from enum import Enum

class GenderEnum(str, Enum):
    male = 'male'
    female = 'female'
    other = 'other'

class CharacterSchema(BaseModel):
    character_id: int | None = None
    character_name: str | None = None
    character_profile: str | None = None
    character_gender: GenderEnum | None = None
    character_personality: str | None = None
    character_details: str | None = None
    user_id: int | None = None

    class Config:
        orm_mode = True
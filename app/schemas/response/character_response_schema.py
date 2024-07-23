from pydantic import BaseModel
from enum import Enum

class CharacterGenderEnum(str, Enum):
    male = 'male'
    female = 'female'
    other = 'other'

class CharacterResponse(BaseModel):
    character_id: int
    character_name: str
    character_profile: str | None = None
    character_gender: CharacterGenderEnum | None = None
    character_personality: str | None = None
    character_details: str | None = None
    user_id: int

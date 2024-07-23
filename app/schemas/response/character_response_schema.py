from enum import Enum
from fastapi_camelcase import CamelModel


class CharacterGenderEnum(str, Enum):
    male = 'male'
    female = 'female'
    other = 'other'

class CharacterResponse(CamelModel):
    character_id: int
    character_name: str
    character_profile: str | None = None
    character_gender: CharacterGenderEnum | None = None
    character_personality: str | None = None
    character_details: str | None = None
    user_id: int

class MessageResponse(CamelModel):
    message: str
from enum import Enum
from fastapi_camelcase import CamelModel

class CharacterGenderEnum(str, Enum):
    male = 'male'
    female = 'female'
    other = 'other'

class CharacterCreate(CamelModel):
    character_name: str
    character_profile: str | None = None
    character_gender: CharacterGenderEnum | None = None
    character_personality: str | None = None
    character_details: str | None = None
    character_is_public: bool
    relationships: list[int] = []

class CharacterUpdate(CamelModel):
    character_name: str | None = None
    character_profile: str | None = None
    character_gender: CharacterGenderEnum | None = None
    character_personality: str | None = None
    character_details: str | None = None
    character_is_public: bool | None = None
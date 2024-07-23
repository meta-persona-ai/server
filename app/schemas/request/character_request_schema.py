from pydantic import ConfigDict
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

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "characterName": "John Doe",
                "characterProfile": "A brave warrior with a mysterious past.",
                "characterGender": "male",
                "characterPersonality": "Brave, Determined, Mysterious",
                "characterDetails": "John has traveled across many lands and fought in countless battles. His true origin remains unknown, but his skills in combat are unparalleled."
            }
        }
    )

class CharacterUpdate(CamelModel):
    character_name: str | None = None
    character_profile: str | None = None
    character_gender: CharacterGenderEnum | None = None
    character_personality: str | None = None
    character_details: str | None = None
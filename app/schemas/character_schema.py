from pydantic import BaseModel, ConfigDict
from enum import Enum

class CharacterGenderEnum(str, Enum):
    male = 'male'
    female = 'female'
    other = 'other'

class CharacterCreate(BaseModel):
    character_name: str
    character_profile: str | None = None
    character_gender: CharacterGenderEnum | None = None
    character_personality: str | None = None
    character_details: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "character_name": "John Doe",
                "character_profile": "A brave warrior with a mysterious past.",
                "character_gender": "male",
                "character_personality": "Brave, Determined, Mysterious",
                "character_details": "John has traveled across many lands and fought in countless battles. His true origin remains unknown, but his skills in combat are unparalleled."
            }
        }
    )

class CharacterResponse(BaseModel):
    character_id: int
    character_name: str
    character_profile: str | None = None
    character_gender: CharacterGenderEnum | None = None
    character_personality: str | None = None
    character_details: str | None = None
    user_id: int

class CharacterUpdate(BaseModel):
    character_name: str | None = None
    character_profile: str | None = None
    character_gender: CharacterGenderEnum | None = None
    character_personality: str | None = None
    character_details: str | None = None
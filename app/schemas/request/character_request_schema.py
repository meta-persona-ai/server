from pydantic import BaseModel, ConfigDict
from enum import Enum

class CharacterGenderEnum(str, Enum):
    male = 'male'
    female = 'female'
    other = 'other'

class CharacterCreate(BaseModel):
    characterName: str
    characterProfile: str | None = None
    characterGender: CharacterGenderEnum | None = None
    characterPersonality: str | None = None
    characterDetails: str | None = None

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

class CharacterUpdate(BaseModel):
    characterName: str | None = None
    characterProfile: str | None = None
    characterGender: CharacterGenderEnum | None = None
    characterPersonality: str | None = None
    characterDetails: str | None = None
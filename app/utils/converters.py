from ..schemas.schemas import CharacterSchema
from ..schemas.request.character_request_schema import CharacterCreate

def convert_create_to_schema(create_schema: CharacterCreate, user_id: int) -> CharacterSchema:
    character = CharacterSchema(
        character_name = create_schema.characterName,
        character_profile = create_schema.characterProfile,
        character_gender = create_schema.characterGender,
        character_personality = create_schema.characterPersonality,
        character_details = create_schema.characterDetails,
        user_id = user_id
    )

    return character
from ..models.character import Character
from ..schemas.schemas import CharacterSchema
from ..schemas.request.character_request_schema import CharacterCreate

def convert_create_to_schema(create_model: CharacterCreate, user_id: int) -> CharacterSchema:
    schema_dict = create_model.model_dump()
    schema_dict['user_id'] = user_id
    
    return CharacterSchema(**schema_dict)

def convert_model_to_schema(character: Character) -> CharacterSchema:
    character = CharacterSchema(
        character_id = character.character_id,
        character_name = character.character_name,
        character_profile = character.character_profile,
        character_gender = character.character_gender,
        character_personality = character.character_personality,
        character_details = character.character_details,
        user_id = character.user_id
    )

    return character

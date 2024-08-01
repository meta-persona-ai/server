from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..models.characters import Character
from ..schemas.request.character_request_schema import CharacterCreate, CharacterUpdate

from ..crud import character_crud


# insert
def create_character(character_create: CharacterCreate, user_id: int, db: Session):
    return character_crud.create_character(character_create, user_id, db)

# select
def get_all_characters(db: Session) -> list[Character]:
    return character_crud.get_all_characters(db)

def get_character(character_id: int, user_id: int, db: Session) -> Character:
    character = character_crud.get_character(character_id, user_id, db)
    if not character:
        raise HTTPException(status_code=404, detail="Characters not found")
    return character

def get_characters_by_id(user_id: int, db: Session) -> list[Character]:
    return character_crud.get_characters_by_user_id(user_id, db)

def get_characters_by_rank(limit: int, db: Session) -> list[Character]:
    return character_crud.get_characters_by_rank(limit, db)

# update
def update_character_by_id(character_id: int, character_data: CharacterUpdate, user_id: int, db: Session) -> Character:
    updated_character = character_crud.update_character_by_id(character_id, character_data, user_id, db)
    if not updated_character:
        raise HTTPException(status_code=404, detail="Character not found or not authorized to update")
    return updated_character

# delete
def delete_character_by_id(character_id: int, user_id: int, db: Session) -> bool:
    success = character_crud.delete_character_by_id(character_id, user_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Character not found or not authorized to delete")
    return success

# deactivate
def deactivate_character_by_id(character_id: int, user_id: int, db: Session) -> Character:
    updated_character = character_crud.deactivate_character_by_id(character_id, user_id, db)
    if not updated_character:
        raise HTTPException(status_code=404, detail="Character not found or not authorized to update")
    return updated_character
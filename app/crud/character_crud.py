from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ..models.character import Character
from ..models.character_relationship import CharacterRelationship
from ..schemas.request.character_request_schema import CharacterCreate, CharacterUpdate

# insert
def create_character(character: CharacterCreate, user_id:int, db: Session) -> Character:
    try:
        db_character = Character(
            character_name=character.character_name,
            character_profile=character.character_profile,
            character_gender=character.character_gender,
            character_personality=character.character_personality,
            character_details=character.character_details,
            character_is_public=character.character_is_public,
            user_id=user_id
        )
        db.add(db_character)
        db.commit()
        db.refresh(db_character)

        # relationships 처리
        for relationship_id in character.relationships:
            character_relationship = CharacterRelationship(
                character_id=db_character.character_id,
                relationship_id=relationship_id
            )
            db.add(character_relationship)
        db.commit()
        db.refresh(db_character)
        return db_character
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")

# select
def get_all_characters(db: Session) -> list[Character]:
    try:
        return db.query(Character).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")

def get_character(character_id: int, db: Session) -> Character:
    try:
        return db.query(Character).filter(Character.character_id == character_id).first()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")

def get_characters_by_user_id(user_id: int, db: Session) -> list[Character]:
    try:
        return db.query(Character).filter(Character.user_id == user_id).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")
    
def get_characters_by_name(character_name: str, db: Session) -> Character:
    try:
        return db.query(Character).filter(Character.character_name == character_name).first()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")

# update
def update_character_by_id(character_id: int, character_data: CharacterUpdate, user_id: int, db: Session) -> Character:
    try:
        character_to_update = db.query(Character).filter(
            Character.character_id == character_id,
            Character.user_id == user_id
        ).first()

        if character_to_update:
            for attr, value in vars(character_data).items():
                if value is not None and attr != "_sa_instance_state":
                    setattr(character_to_update, attr, value)
            db.commit()
            db.refresh(character_to_update)
            return character_to_update

        return None
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")

# delete
def delete_character_by_id(character_id: int, user_id: int, db: Session) -> bool:
    try:
        character_to_delete = db.query(Character).filter(
            Character.character_id == character_id,
            Character.user_id == user_id
        ).first()
        
        if character_to_delete:
            db.delete(character_to_delete)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")
    

# deactivate
def deactivate_character_by_id(character_id:int, user_id: int, db: Session):
    character_to_deactivate = db.query(Character).filter(
        Character.character_id == character_id,
        Character.user_id == user_id).first()
    if character_to_deactivate:
        character_to_deactivate.character_is_active = False
        db.commit()
        return character_to_deactivate
    return None
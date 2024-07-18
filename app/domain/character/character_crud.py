from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ...models.character import Character
from ...schemas.character_schema import CharacterCreate, CharacterUpdate

# insert
def create_character(character: CharacterCreate, user_id: int, db: Session) -> Character:
    try:
        db_character = Character(
            character_name=character.character_name,
            character_profile=character.character_profile,
            character_gender=character.character_gender,
            character_personality=character.character_personality,
            character_details=character.character_details,
            user_id=user_id
        )
        db.add(db_character)
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

def get_characters_by_id(user_id: int, db: Session) -> list[Character]:
    try:
        return db.query(Character).filter(Character.user_id == user_id).all()
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

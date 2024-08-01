from sqlalchemy import desc
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ..models.characters import Character
from ..models.character_relationships import CharacterRelationship
from ..schemas.request.character_request_schema import CharacterCreate, CharacterUpdate

# insert
def create_character(character: CharacterCreate, user_id: int, db: Session) -> Character:
    """
    새로운 캐릭터를 생성하고 데이터베이스에 저장합니다.

    Args:
        character (CharacterCreate): 생성할 캐릭터의 데이터.
        user_id (int): 캐릭터를 생성하는 사용자의 ID.
        db (Session): 데이터베이스 세션.

    Returns:
        Character: 생성된 캐릭터 객체.

    Raises:
        HTTPException: 데이터베이스 오류 발생 시 예외를 발생시킵니다.
    """
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

        # 관계 설정 처리
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
    """
    공개된 모든 캐릭터를 조회합니다.

    Args:
        db (Session): 데이터베이스 세션.

    Returns:
        list[Character]: 공개된 캐릭터 목록.

    Raises:
        HTTPException: 데이터베이스 오류 발생 시 예외를 발생시킵니다.
    """
    try:
        return db.query(Character).filter(
            Character.character_is_public == True,
            Character.is_active()
        ).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")

def get_character(character_id: int, user_id: int, db: Session) -> Character:
    """
    특정 캐릭터를 조회합니다. 캐릭터가 공개되어 있거나 사용자가 소유한 캐릭터만 조회됩니다.

    Args:
        character_id (int): 조회할 캐릭터의 ID.
        user_id (int): 요청한 사용자의 ID.
        db (Session): 데이터베이스 세션.

    Returns:
        Character: 조회된 캐릭터 객체.

    Raises:
        HTTPException: 캐릭터를 찾을 수 없거나 데이터베이스 오류 발생 시 예외를 발생시킵니다.
    """
    try:
        character = db.query(Character).filter(
            Character.character_id == character_id,
            (Character.character_is_public == True) | (Character.user_id == user_id),
            Character.is_active()
        ).first()
        if not character:
            raise HTTPException(status_code=404, detail="캐릭터를 찾을 수 없습니다")
        return character
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")

def get_characters_by_user_id(user_id: int, db: Session) -> list[Character]:
    """
    특정 사용자가 소유한 캐릭터 목록을 조회합니다.

    Args:
        user_id (int): 캐릭터를 조회할 사용자의 ID.
        db (Session): 데이터베이스 세션.

    Returns:
        list[Character]: 사용자가 소유한 캐릭터 목록.

    Raises:
        HTTPException: 데이터베이스 오류 발생 시 예외를 발생시킵니다.
    """
    try:
        return db.query(Character).filter(
            Character.user_id == user_id,
            Character.is_active()
        ).order_by(desc(Character.character_created_at)).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")

def get_characters_by_name(character_name: str, db: Session) -> Character:
    """
    캐릭터 이름으로 캐릭터를 조회합니다.

    Args:
        character_name (str): 조회할 캐릭터의 이름.
        db (Session): 데이터베이스 세션.

    Returns:
        Character: 조회된 캐릭터 객체.

    Raises:
        HTTPException: 데이터베이스 오류 발생 시 예외를 발생시킵니다.
    """
    try:
        return db.query(Character).filter(
            Character.character_name == character_name,
            Character.is_active()
        ).first()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")
    
def get_characters_by_rank(limit: int, db: Session) -> list[Character]:
    """
    사용 횟수가 높은 상위 5개의 공개된 캐릭터를 조회합니다.

    Args:
        db (Session): 데이터베이스 세션.

    Returns:
        list[Character]: 사용 횟수에 따라 내림차순으로 정렬된 상위 5개의 캐릭터 목록.

    Raises:
        HTTPException: 데이터베이스 오류 발생 시 예외를 발생시킵니다.
    """
    try:
        return db.query(Character).filter(
            Character.character_is_public == True,
            Character.is_active()
        ).order_by(desc(Character.character_usage_count)).limit(limit).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")


# update
def update_character_by_id(character_id: int, character_data: CharacterUpdate, user_id: int, db: Session) -> Character:
    """
    캐릭터의 정보를 업데이트합니다.

    Args:
        character_id (int): 업데이트할 캐릭터의 ID.
        character_data (CharacterUpdate): 업데이트할 데이터.
        user_id (int): 캐릭터 소유자의 ID.
        db (Session): 데이터베이스 세션.

    Returns:
        Character: 업데이트된 캐릭터 객체. 

    Raises:
        HTTPException: 데이터베이스 오류 발생 시 예외를 발생시킵니다.
    """
    try:
        character_to_update = db.query(Character).filter(
            Character.character_id == character_id,
            Character.user_id == user_id,
            Character.is_active()
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
    """
    캐릭터를 데이터베이스에서 삭제합니다.

    Args:
        character_id (int): 삭제할 캐릭터의 ID.
        user_id (int): 캐릭터 소유자의 ID.
        db (Session): 데이터베이스 세션.

    Returns:
        bool: 캐릭터 삭제 성공 여부.

    Raises:
        HTTPException: 데이터베이스 오류 발생 시 예외를 발생시킵니다.
    """
    try:
        character_to_delete = db.query(Character).filter(
            Character.character_id == character_id,
            Character.user_id == user_id,
            Character.is_active()
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
def deactivate_character_by_id(character_id: int, user_id: int, db: Session):
    """
    캐릭터를 비활성화 상태로 변경합니다.

    Args:
        character_id (int): 비활성화할 캐릭터의 ID.
        user_id (int): 캐릭터 소유자의 ID.
        db (Session): 데이터베이스 세션.

    Returns:
        Character: 비활성화된 캐릭터 객체. 비활성화할 캐릭터가 없으면 None을 반환합니다.
    """
    character_to_deactivate = db.query(Character).filter(
        Character.character_id == character_id,
        Character.user_id == user_id,
        Character.is_active()
    ).first()
    if character_to_deactivate:
        character_to_deactivate.character_is_active = False
        db.commit()
        return character_to_deactivate
    return None

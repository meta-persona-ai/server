from fastapi import APIRouter, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.database import get_db
from app.lib import jwt_util
from app.schemas.character_schema import CharacterCreate, CharacterResponse, CharacterUpdate

from ...services import character_service

router = APIRouter(
    prefix="/api/characters",
    tags=["Characters"]
)
api_key_header = APIKeyHeader(name="Authorization")

@router.post("/",
             description="새 캐릭터를 생성하는 API입니다.",
             response_model=CharacterResponse
            )
async def create_character(character: CharacterCreate, authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    payload = jwt_util.decode_token(authorization)
    return character_service.create_character(character, payload.id, db)

@router.get("/",
            description="모든 캐릭터를 조회하는 API입니다.",
            response_model=list[CharacterResponse]
            )
async def get_all_characters(db: Session = Depends(get_db)):
    return character_service.get_all_characters(db)

@router.get("/me",
            description="인증된 사용자의 모든 캐릭터를 조회하는 API입니다.",
            response_model=list[CharacterResponse]
            )
async def get_my_characters(authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    payload = jwt_util.decode_token(authorization)
    return character_service.get_characters_by_id(payload.id, db)

@router.put("/{character_id}",
            description="특정 캐릭터 정보를 업데이트하는 API입니다.",
            response_model=CharacterResponse
            )
async def update_character(character_id: int, character_update: CharacterUpdate, authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    payload = jwt_util.decode_token(authorization)
    updated_character = character_service.update_character_by_id(character_id, character_update, payload.id, db)
    return updated_character

@router.delete("/{character_id}",
               description="특정 캐릭터를 삭제하는 API입니다.",
               response_model=dict
               )
async def delete_character(character_id: int, authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    payload = jwt_util.decode_token(authorization)
    success = character_service.delete_character_by_id(character_id, payload.id, db)
    return {"message": "Character deleted successfully"} if success else {"message": "Character deletion failed"}

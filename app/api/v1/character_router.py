from fastapi import APIRouter, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.utils import jwt_util
from app.schemas.request.character_request_schema import CharacterCreate, CharacterUpdate
from app.schemas.response.character_response_schema import CharacterResponse, MessageResponse

from ...services import character_service

router = APIRouter(
    prefix="/api/characters",
    tags=["Characters"]
)
api_key_header = APIKeyHeader(name="Authorization")

@router.post("/",
            description="새 캐릭터를 생성하는 API입니다.",
            response_model=dict
            )
async def create_character(character: CharacterCreate, authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    payload = jwt_util.decode_token(authorization)
    success = character_service.create_character(character, payload.id, db)
    return {"message": "Character created successfully"} if success else {"message": "Character creation failed"}

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
            response_model=MessageResponse
            )
async def update_character(character_id: int, character_update: CharacterUpdate, authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    payload = jwt_util.decode_token(authorization)
    success = character_service.update_character_by_id(character_id, character_update, payload.id, db)
    return {"message": "Character updated successfully"} if success else {"message": "Character update failed"}

@router.delete("/{character_id}",
               description="특정 캐릭터를 삭제하는 API입니다.",
               response_model=MessageResponse
               )
async def delete_character(character_id: int, authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    payload = jwt_util.decode_token(authorization)
    success = character_service.delete_character_by_id(character_id, payload.id, db)
    return {"message": "Character deleted successfully"} if success else {"message": "Character deletion failed"}

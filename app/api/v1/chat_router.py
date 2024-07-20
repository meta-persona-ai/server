from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.lib import jwt_util
from app.schemas.chat_schema import ChatCreate, ChatResponse
from app.services import chat_service, character_service


router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"]
)
api_key_header = APIKeyHeader(name="Authorization")

@router.post("/",
            description="새 채팅방을 생성하는 API입니다.",
            response_model=ChatResponse
            )
async def create_chat(character_id: int, authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    character = character_service.get_characters_by_id(character_id, db)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    payload = jwt_util.decode_token(authorization)
    chat = ChatCreate(user_id=payload.id, character_id=character_id)
    return chat_service.create_chat(chat, db)

@router.get("/me",
            description="인증된 사용자의 모든 채팅방를 조회하는 API입니다.",
            )
async def get_my_chat(authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    payload = jwt_util.decode_token(authorization)
    return chat_service.get_chats_by_id(payload.id, db)

@router.delete("/{chat_id}",
               description="특정 캐릭터를 삭제하는 API입니다.",
               response_model=dict
               )
async def delete_character(chat_id: int, authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    payload = jwt_util.decode_token(authorization)
    success = chat_service.delete_chat_by_id(chat_id, payload.id, db)
    return {"message": "Character deleted successfully"} if success else {"message": "Character deletion failed"}

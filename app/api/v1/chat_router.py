from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.utils import jwt_util
from app.schemas.request.chat_request_schema import ChatCreate
from app.schemas.response.chat_response_schema import MessageResponse
from app.services import chat_service, character_service


router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"]
)
api_key_header = APIKeyHeader(name="Authorization")

@router.post("/",
            description="새 채팅방을 생성하는 API입니다.",
            response_model=MessageResponse
            )
async def create_chat(character_id: int, authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    character = character_service.get_characters_by_id(character_id, db)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    payload = jwt_util.decode_token(authorization)
    chat = ChatCreate(user_id=payload.id, character_id=character_id)
    success = chat_service.create_chat(chat, db)
    return {"message": "Chat created successfully"} if success else {"message": "Chat creation failed"}

@router.get("/me",
            description="인증된 사용자의 모든 채팅방를 조회하는 API입니다.",
            )
async def get_my_chat(authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    payload = jwt_util.decode_token(authorization)
    return chat_service.get_chats_by_user_id(payload.id, db)

@router.delete("/{chat_id}",
               description="특정 채팅방을 삭제하는 API입니다.",
               response_model=MessageResponse
               )
async def delete_chat(chat_id: int, authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    payload = jwt_util.decode_token(authorization)
    success = chat_service.delete_chat_by_id(chat_id, payload.id, db)
    return {"message": "Chat deleted successfully"} if success else {"message": "Chat deletion failed"}

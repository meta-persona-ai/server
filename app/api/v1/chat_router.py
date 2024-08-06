from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core import get_current_user
from app.schemas.request.chat_request_schema import ChatCreate
from app.schemas.response.chat_response_schema import ChatResponse, MessageResponse, ChatCreateResponse
from app.services import ChatService, CharacterService

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"]
)

@router.post("/",
            description="새 채팅방을 생성하는 API입니다.",
            response_model=ChatCreateResponse
            )
async def create_chat(character_id: int, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    character = CharacterService.get_characters_by_id(character_id, db)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    chat = ChatCreate(user_id=user_id, character_id=character_id)
    chat = ChatService.create_chat(chat, db)
    return {
        "message": "Chat created successfully",
        "chat_id": chat.chat_id
        }

@router.get("/me/",
            description="인증된 사용자의 모든 채팅방를 조회하는 API입니다.",
            response_model=list[ChatResponse]
            )
async def get_my_chat(user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return ChatService.get_chats_by_user_id(user_id, db)

@router.delete("/{chat_id}",
               description="특정 채팅방을 삭제하는 API입니다.",
               response_model=MessageResponse
               )
async def delete_chat(chat_id: int, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    success = ChatService.delete_chat_by_id(chat_id, user_id, db)
    return {"message": "Chat deleted successfully"} if success else {"message": "Chat deletion failed"}

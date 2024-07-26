from fastapi import APIRouter, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.utils import jwt_util

from app.services import chat_log_service
from app.schemas.response.chat_response_schema import MessageResponse



router = APIRouter(
    prefix="/api/v1/chat-log",
    tags=["Chat log"]
)
api_key_header = APIKeyHeader(name="Authorization")


@router.get("/me/{chat_id}",
            )
async def get_chat_logs_by_chat_id_and_user_id(chat_id: int, authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    payload = jwt_util.decode_token(authorization)
    return chat_log_service.get_chat_logs_by_chat_id_and_user_id(chat_id, payload.id, db)

@router.delete("/{log_id}",
               description="특정 채팅방을 삭제하는 API입니다.",
               response_model=MessageResponse
               )
async def delete_chat(log_id: int, authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    payload = jwt_util.decode_token(authorization)
    chat_log_service.delete_chat_log_by_id(log_id, payload.id, db)
    return {"message": "Chat deleted successfully"}

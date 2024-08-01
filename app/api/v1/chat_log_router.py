from fastapi import APIRouter, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.utils import jwt_util

from app.services import chat_log_service
from app.schemas.response.chat_log_resposne_schema import ChatLogResponse, MessageResponse



router = APIRouter(
    prefix="/api/v1/chat-log",
    tags=["Chat log"]
)
api_key_header = APIKeyHeader(name="Authorization")


@router.get("/me/{chat_id}",
            response_model=list[ChatLogResponse]
            )
async def get_chat_logs_by_chat_id_and_user_id(chat_id: int, authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    payload = jwt_util.verify_token(authorization)
    return chat_log_service.get_chat_logs_by_chat_id_and_user_id(chat_id, payload.id, db)

@router.delete("/{log_id}",
               response_model=MessageResponse
               )
async def delete_chat(log_id: int, authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    payload = jwt_util.verify_token(authorization)
    chat_log_service.delete_chat_log_by_id(log_id, payload.id, db)
    return {"message": "Log deleted successfully"}

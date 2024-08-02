from fastapi import APIRouter, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import get_current_user

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
async def get_chat_logs_by_chat_id_and_user_id(chat_id: int, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return chat_log_service.get_chat_logs_by_chat_id_and_user_id(chat_id, user_id, db)

@router.delete("/{log_id}",
               response_model=MessageResponse
               )
async def delete_chat(log_id: int, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    chat_log_service.delete_chat_log_by_id(log_id, user_id, db)
    return {"message": "Log deleted successfully"}

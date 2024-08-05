from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..crud import chat_log_crud
from ..schemas.request.chat_log_request_schema import ChatLogCreate

from .chat_service import ChatService

class ChatLogService:
    # insert
    @staticmethod
    def create_chat_log(log: ChatLogCreate, db: Session):
        return chat_log_crud.create_chat_log(log, db)

    # select
    @staticmethod
    def get_chat_logs_by_chat_id_and_user_id(chat_id: int, user_id: int, db: Session):
        chat = ChatService.get_chat_by_chat_id_and_user_id(chat_id, user_id, db)
        if not chat:
            raise HTTPException(status_code=404, detail="Chats not found")

        chat_logs = chat_log_crud.get_chat_logs_by_user_id(chat_id, user_id, db)
        if not chat_logs:
            raise HTTPException(status_code=404, detail="Chat logs not found")
        return chat_logs

    # delete
    @staticmethod
    def delete_chat_log_by_id(log_id: int, user_id: int, db: Session) -> bool:
        success = chat_log_crud.delete_chat_log_by_id(log_id, user_id, db)
        if not success:
            raise HTTPException(status_code=404, detail="Log not found or not authorized to delete")
        return success

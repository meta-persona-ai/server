from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..crud import chat_log_crud
from ..schemas.request.chat_log_request_schema import ChatLogCreate


# insert
def create_chat_log(log: ChatLogCreate, db: Session):
    return chat_log_crud.create_chat_log(log, db)

# select
def get_chat_logs_by_user_id(chat_id: int, user_id: int, db: Session):
    chat_logs = chat_log_crud.get_chat_logs_by_user_id(chat_id, user_id, db)
    if not chat_logs:
        raise HTTPException(status_code=404, detail="Chat logs not found")
    return chat_logs

# def get_chats_by_chat_id_and_user_id(chat_id: int, user_id: int, db: Session) -> Chat:
#     return chat_crud.get_chats_by_chat_id_and_user_id(chat_id, user_id, db)

# # delete
# def delete_chat_by_id(chat_id: int, user_id: int, db: Session) -> bool:
#     success = chat_crud.delete_chat_by_id(chat_id, user_id, db)
#     if not success:
#         raise HTTPException(status_code=404, detail="Chat not found or not authorized to delete")
#     return success

from sqlalchemy.orm import Session

from ..crud import chat_crud
from ..schemas.chat_schema import ChatCreate


# insert
def create_chat(chat: ChatCreate, db: Session):
    return chat_crud.create_chat(chat, db)

# # select
# def get_users(db: Session) -> list[User]:
#     return chat_crud.get_all_users(db)

# def get_user_by_id(user_id: int, db: Session) -> User:
#     return chat_crud.get_user_by_id(user_id, db)

# def get_user_by_email(email: str, db: Session) -> User:
#     return chat_crud.get_user_by_email(email, db)

# # update
# def update_user_by_id(user_id: int, user_data: UserUpdate, db: Session) -> User:
#     return chat_crud.update_user_by_id(user_id, user_data, db)

# # delete
# def delete_user_by_id(user_id: int, db: Session) -> bool:
#     return chat_crud.delete_user_by_id(user_id, db)

# # deactivate
# def deactivate_user_by_id(user_id: int, db: Session) -> bool:
#     return chat_crud.deactivate_user_by_id(user_id, db)
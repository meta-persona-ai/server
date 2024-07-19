from sqlalchemy.orm import Session

from ..crud import user_crud
from ..models.user import User
from ..schemas.user_request_schema import UserUpdate


# select
def get_users(db: Session) -> list[User]:
    return user_crud.get_all_users(db)

def get_user_by_id(user_id: int, db: Session) -> User:
    return user_crud.get_user_by_id(user_id, db)

def get_user_by_email(email: str, db: Session) -> User:
    return user_crud.get_user_by_email(email, db)

# update
def update_user_by_id(user_id: int, user_data: UserUpdate, db: Session) -> User:
    return user_crud.update_user_by_id(user_id, user_data, db)

# delete
def delete_user_by_id(user_id: int, db: Session) -> bool:
    return user_crud.delete_user_by_id(user_id, db)

# deactivate
def deactivate_user_by_id(user_id: int, db: Session) -> bool:
    return user_crud.deactivate_user_by_id(user_id, db)
from sqlalchemy.orm import Session

from . import user_crud
from models.user_model import User


def get_users(db: Session) -> list[User]:
    return user_crud.get_all_users(db)

def get_user_by_id(user_id: int, db: Session) -> User:
    return user_crud.get_user_by_id(user_id, db)

def get_user_by_email(email: str, db: Session) -> User:
    return user_crud.get_user_by_email(email, db)

def delete_user_by_id(user_id: int, db: Session) -> bool:
    return user_crud.delete_user_by_id(user_id, db)
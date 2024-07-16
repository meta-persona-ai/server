from sqlalchemy.orm import Session

from . import user_crud


def get_all_users(db: Session):
    return user_crud.get_all_users(db)
from sqlalchemy.orm import Session

from ..crud import user_crud
from ..models import User
from ..schemas.request.user_request_schema import UserUpdate

class UserService:
    # select
    @staticmethod
    def get_users(db: Session) -> list[User]:
        return user_crud.get_all_users(db)

    @staticmethod
    def get_user_by_id(user_id: int, db: Session) -> User:
        return user_crud.get_user_by_id(user_id, db)

    @staticmethod
    def get_user_by_email(email: str, db: Session) -> User:
        return user_crud.get_user_by_email(email, db)

    # update
    @staticmethod
    def update_user_by_id(user_id: int, user_data: UserUpdate, db: Session) -> User:
        return user_crud.update_user_by_id(user_id, user_data, db)

    # delete
    @staticmethod
    def delete_user_by_id(user_id: int, db: Session) -> bool:
        return user_crud.delete_user_by_id(user_id, db)

    # deactivate
    @staticmethod
    def deactivate_user_by_id(user_id: int, db: Session) -> bool:
        return user_crud.deactivate_user_by_id(user_id, db)
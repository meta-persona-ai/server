from sqlalchemy.orm import Session

from ...models.user import User
from ...schemas.user_schema import UserCreate


def create_user(db: Session, user: UserCreate):
    db_user = User(
        user_email=user.user_email,
        user_password=user.user_password,
        user_name=user.user_name,
        user_profile=user.user_profile
    )
    db.add(db_user)
    db.commit()
    return db_user
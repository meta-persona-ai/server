from sqlalchemy.orm import Session

from ...models.user import User
from ...schemas import auth_schema


def create_user(db: Session, user: auth_schema.UserCreate):
    db_user = User(
        user_email=user.email,
        user_password=user.hashed_password,
        user_name=user.name,
        user_profile=user.picture
    )
    db.add(db_user)
    db.commit()
    return db_user
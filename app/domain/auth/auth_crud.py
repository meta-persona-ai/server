from sqlalchemy.orm import Session

from models import user_model
from . import auth_schema


def create_user(db: Session, user: auth_schema.UserCreate):
    db_user = user_model.User(
        email=user.email,
        hashed_password=user.hashed_password,
        name=user.name,
        picture=user.picture,
        is_active=user.is_active
    )
    db.add(db_user)
    db.commit()
    return db_user
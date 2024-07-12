from sqlalchemy.orm import Session

from ..models import user_model
from ..schemas import user_schema


# def get_user(db: Session, user_id: int):
#     return db.query(user.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(user_model.User).filter(user_model.User.email == email).first()


def get_users(db: Session):
    return db.query(user_model.User).all()


def create_user(db: Session, user: user_schema.UserCreate):
    db_user = user_model.User(
        email=user.email,
        hashed_password=user.hashed_password,
        name=user.name,
        picture=user.picture,
        is_active=user.is_active
    )
    db.add(db_user)
    db.commit()
    # 세션을 닫기 전에 유효한 데이터로 반환
    return db_user


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: user_schema.User, user_id: int):
#     db_item = user_model.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
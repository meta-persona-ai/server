from sqlalchemy.orm import Session
import os

from ...core.logger_config import setup_logger
from ...lib import google_api
from ...lib import jwt_util
from . import auth_crud
from ..user import user_service
from ...schemas.auth_schema import UserCreate


logger = setup_logger()


def login_google() -> str:
    return google_api.get_google_login_url()


def auth_google_web(code: str, db: Session):
    access_token = google_api.get_google_token(code)
    user = google_api.get_google_user_data(access_token)

    return sign_in_or_login(user, db)


def auth_google_id_token(id_token: str, db: Session):
    user = google_api.decode_id_token(id_token)

    return sign_in_or_login(user, db)


def sign_in_or_login(user: UserCreate, db: Session):
    existing_user = user_service.get_user_by_email(user.user_email, db)
    if existing_user:
        db_user = existing_user
    else:
        db_user = auth_crud.create_user(db, user)

        logger.info(f"📌 successfully make user - id: {db_user.user_id}, name: {db_user.user_name}, email: {db_user.user_email}")

    logger.info(f"📌 login complete!")

    return jwt_util.make_access_token(db_user)


def make_test_access_token(db: Session):
    test_email = "test@example.com"

    existing_user = user_service.get_user_by_email(test_email, db)

    if existing_user:
        db_user = existing_user
    else:
        test_user = UserCreate(user_email="test@example.com", user_password="test", user_name="Test User", user_profile="test.jpg")
        db_user = auth_crud.create_user(db, test_user)

    return jwt_util.make_access_token(db_user)

def decode_token(token: str):
    return jwt_util.decode_token(token)
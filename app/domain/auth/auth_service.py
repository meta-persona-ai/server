from sqlalchemy.orm import Session
import os

from ...core.logger_config import setup_logger
from ...lib.google_api import get_google_login_url, get_google_token, get_google_user_data, decode_id_token
from ...lib.jwt_util import make_access_token, decode_token
from . import auth_crud
from ..user import user_service


logger = setup_logger()


def login_google() -> str:
    return get_google_login_url()


def auth_google(code: str, db: Session):
    access_token = get_google_token(code)

    return auth_google_access_token(access_token, db)

def auth_google_access_token(access_token: str, db: Session):
    user_data = get_google_user_data(access_token)

    logger.info(f"📌 get user data to google - {user_data}")

    existing_user = user_service.get_user_by_email(user_data.email, db)
    

    if existing_user:
        db_user = existing_user
    else:
        db_user = auth_crud.create_user(db, user_data)

        logger.info(f"📌 successfully make user - {db_user}")

    logger.info(f"📌 login complete!")

    return make_access_token(db_user)

def auth_google_id_token(id_token: str, db: Session):
    user_info = decode_id_token(id_token)

    logger.info(f"📌 get user info to google id token - {user_info}")

    # existing_user = user_service.get_user_by_email(user_data.email, db)
    

    # if existing_user:
    #     db_user = existing_user
    # else:
    #     db_user = auth_crud.create_user(db, user_data)

    #     logger.info(f"📌 successfully make user - {db_user}")

    # logger.info(f"📌 login complete!")

    # return make_access_token(db_user)

def decode_token(token: str):
    return decode_token(token)
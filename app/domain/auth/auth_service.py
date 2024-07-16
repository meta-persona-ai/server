from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import jwt
import os

from core.logger_config import setup_logger
from lib.google_api import get_google_login_url, get_google_token, get_google_user_data
from models.user_model import User
from . import auth_crud
from ..user import user_service


logger = setup_logger()

load_dotenv()
JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')


def login_google() -> str:
    return get_google_login_url()


def auth_google(code: str, db: Session):
    access_token = get_google_token(code)

    return auth_google_access_token(access_token, db)

def auth_google_access_token(access_token: str, db: Session):
    user_data = get_google_user_data(access_token)

    existing_user = user_service.get_user_by_email(user_data.email, db)
    
    if existing_user:
        db_user = existing_user
    else:
        db_user = auth_crud.create_user(db, user_data)

    return make_access_token(db_user)

def make_access_token(user: User):
    return jwt.encode({
        "sub": user.id,
        "name": user.name,
        "email": user.email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token: str):
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    logger.info(f"📌 token - {payload}")
    return payload

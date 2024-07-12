from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import requests
import jwt
import os

from ...core.logger_config import setup_logger
from . import auth_crud, auth_schema


logger = setup_logger()

load_dotenv()
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI')
JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')


def login_google() -> str:
    return f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"


def auth_google(code: str, db: Session) -> str:
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    token_response = response.json()
    access_token = token_response.get("access_token")
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
    user_info_response = user_info.json()

    user_data = {
        "email": user_info_response.get("email"),
        "name": user_info_response.get("name"),
        "picture": user_info_response.get("picture"),
        "is_active": True,
        "hashed_password": None
    }
    
    user = auth_schema.UserCreate(**user_data)
    auth_crud.create_user(db, user)
    
    jwt_token = jwt.encode({
        "sub": user_info_response["id"],
        "name": user_info_response["name"],
        "email": user_info_response["email"],
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return jwt_token

def decode_token(token: str):
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    logger.info(f"📌 token - {payload}")
    return payload

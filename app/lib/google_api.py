from dotenv import load_dotenv
import requests
import os
import jwt
from jwt import PyJWKClient

from ..core.logger_config import setup_logger
from ..schemas.auth_schema import UserCreate

load_dotenv()
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_ID2 = os.getenv('GOOGLE_CLIENT_ID2')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI')

logger = setup_logger()

def get_google_login_url() -> str:
    return f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"

def get_google_token(code: str) -> str:
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

    return access_token

def get_google_user_data(access_token: str) -> UserCreate:
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
    user_info_response = user_info.json()

    logger.info(f"📌 user info - {user_info_response}")
    
    user_data = {
        "email": user_info_response.get("email"),
        "name": user_info_response.get("name"),
        "picture": user_info_response.get("picture"),
        "is_active": True,
        "hashed_password": None
    }

    user = UserCreate(**user_data)
    return user

def decode_id_token(id_token: str) -> UserCreate:
    """
    ID 토큰을 디코딩하고 검증하여 사용자 정보를 추출합니다.
    """
    jwks_url = "https://www.googleapis.com/oauth2/v3/certs"
    jwks_client = PyJWKClient(jwks_url)

    signing_key = jwks_client.get_signing_key_from_jwt(id_token)
    
    user_info = jwt.decode(id_token, signing_key.key, algorithms=["RS256"], audience=GOOGLE_CLIENT_ID2)
    
    user_data = {
        "id": int(user_info.get("sub")),
        "user_email": user_info.get("email"),
        "user_name": user_info.get("name"),
        "user_profile": user_info.get("picture"),
    }
    user = UserCreate(**user_data)
    return user
from datetime import datetime, timedelta, timezone
import jwt
import pytz
from dotenv import load_dotenv
import os

from ..models.user import User
from app.schemas.user_schema import UserSchema


load_dotenv()
JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')


def make_access_token(user: User) -> str:
    return jwt.encode({
        "id": user.user_id,
        "name": user.user_name,
        "email": user.user_email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(authorization: str) -> UserSchema:
    token = authorization.split(" ")[1]  # "Bearer " 부분을 제거
    decoded_payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    payload = UserSchema(**decoded_payload)
    
    # JWT 발급 시점과 현재 서버 시간 프린트
    token_iat = datetime.fromtimestamp(decoded_payload['iat'], tz=pytz.UTC)
    current_time = datetime.now(tz=pytz.UTC)
    
    print(f"JWT 발급 시점 (iat): {token_iat}")
    print(f"현재 서버 시간: {current_time}")

    return payload
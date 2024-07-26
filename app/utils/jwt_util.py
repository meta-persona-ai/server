from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

from ..models.user import User
from app.schemas.schemas import UserSchema
from pydantic import BaseModel


load_dotenv()
JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

class TokenData(BaseModel):
    id: int
    email: str
    name: str
    picture: str | None = None

def make_access_token(user: User) -> str:
    return jwt.encode({
        "id": user.user_id,
        "name": user.user_name,
        "email": user.user_email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(authorization: str) -> UserSchema:
    token = authorization.split(" ")[1]  # "Bearer " 부분을 제거
    payload = UserSchema(**jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM]))
    return payload


def verify_token(token: str) -> TokenData:
    try:
        token = token.split(" ")[1]  # "Bearer " 부분을 제거
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("id")
        if user_id is None:
            raise credentials_exception
        
        token_data = TokenData(**payload)
    except JWTError:
        raise credentials_exception
    return token_data
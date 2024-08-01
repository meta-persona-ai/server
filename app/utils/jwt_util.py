from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from jose import JWTError, jwt

from ..core.logger_config import setup_logger
from ..core.env_config import settings
from ..models.user import User


logger = setup_logger()

JWT_SECRET = settings.jwt_secret
JWT_ALGORITHM = settings.jwt_algorithm

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

class TokenData(BaseModel):
    id: int
    email: str
    name: str

def make_access_token(user: User) -> str:
    return jwt.encode({
        "id": user.user_id,
        "name": user.user_name,
        "email": user.user_email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(authorization: str) -> TokenData:
    token = authorization.split(" ")[1]
    logger.warning(f"⚠️ {token}")
    payload = TokenData(**jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM]))
    return payload


def verify_token(token: str) -> TokenData:
    try:
        token = token.split(" ")[1]  # "Bearer " 부분을 제거
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("id")
        if user_id is None:
            logger.error("❌ User ID is missing in token payload.")
            raise credentials_exception
        
        token_data = TokenData(**payload)
    except JWTError:
        logger.error("❌ Token decoding failed. Invalid token.")
        raise credentials_exception
    except IndexError:
        logger.error("❌ Token decoding failed. Invalid token.")
        raise credentials_exception
    return token_data
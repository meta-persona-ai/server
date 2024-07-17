from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt

from ...database import get_db
from ...schemas.auth import auth_request_schema
from . import auth_service

router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/test/login/google")
async def login_google():
    login_url = auth_service.login_google()
    return {
        "url": login_url
    }

@router.get("/test/google")
async def auth_google(code: str, db: Session = Depends(get_db)):
    jwt_token = auth_service.auth_google(code, db)
    return {
        "jwt_token": jwt_token,
    }

@router.get("/token",
            description="발급된 access-token에서 사용자 정보를 반환합니다."
            )
async def get_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = auth_service.decode_token(token)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ===================================================================

@router.post("/login/google/code", 
            description="구글 로그인시 발급되는 code를 사용합니다."
            )
async def auth_google_code(data: auth_request_schema.LoginGoogleCode, db: Session = Depends(get_db)):
    jwt_token = auth_service.auth_google(data.code, db)
    return {
        "jwt_token": jwt_token,
    }

@router.post("/login/google/access-token", 
            description="구글 로그인시 발급되는 access-token를 사용합니다."
            )
async def auth_google_token(data: auth_request_schema.LoginGoogleToken, db: Session = Depends(get_db)):
    jwt_token = auth_service.auth_google_access_token(data.token, db)
    return {
        "jwt_token": jwt_token,
    }
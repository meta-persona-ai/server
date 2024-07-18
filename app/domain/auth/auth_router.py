from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from sqlalchemy.orm import Session
import jwt

from ...database import get_db
from ...core.logger_config import setup_logger
from ...schemas.auth import auth_request_schema
from . import auth_service

logger = setup_logger()

router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
api_key_header = APIKeyHeader(name="Authorization")


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



# ===================================================================

@router.post("/login/google/code", 
            description="구글 로그인시 발급되는 code를 사용합니다."
            )
async def auth_google_code(data: auth_request_schema.LoginGoogleCode, db: Session = Depends(get_db)):
    logger.info(f"📌 auth_google_code - {data}")

    jwt_token = auth_service.auth_google_id_token(data.code, db)
    logger.info(f"📌 return jwt token - {jwt_token}")

    return {
        "jwt_token": jwt_token,
    }

@router.post("/login/google/id-token", 
            description="구글 로그인시 발급되는 id-token를 사용하여 로그인합니다."
            )
async def auth_google_token(data: auth_request_schema.LoginGoogleIdToken, db: Session = Depends(get_db)):
    logger.info(f"📌 /login/google/id-token - {data}")
    jwt_token = auth_service.auth_google_id_token(data.id_token, db)
    # return {
    #     "jwt_token": jwt_token,
    # }

# ===================================================================

@router.post("/test/access-token", 
            description="테스트용 access-token을 반환합니다."
            )
async def auth_google_token(db: Session = Depends(get_db)):
    jwt_token = auth_service.make_test_access_token(db)
    return {
        "jwt_token": jwt_token,
    }

@router.get("/token",
            description="발급된 access-token에서 사용자 정보를 반환합니다."
            )
async def get_token(token: str = Depends(api_key_header)):
    try:
        payload = auth_service.decode_token(token)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
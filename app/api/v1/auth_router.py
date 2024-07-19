from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
import jwt

from ...database import get_db
from ...core.logger_config import setup_logger
from ...schemas import auth_request_schema
from ...services import auth_service


logger = setup_logger()
api_key_header = APIKeyHeader(name="Authorization")

router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)


@router.get("/login/google",
            description="구글 로그인 URL을 반환합니다.")
async def get_google_login_url():
    login_url = auth_service.login_google()
    return {
        "url": login_url
    }

@router.get("/login/google/callback",
            description="구글 로그인 후 콜백으로 받은 코드를 사용하여 인증합니다.")
async def auth_google_callback(code: str, db: Session = Depends(get_db)):
    jwt_token = auth_service.auth_google_web(code, db)
    return {
        "jwt_token": jwt_token,
    }

@router.post("/login/google/code",
             description="구글 로그인시 발급되는 code를 사용하여 인증합니다.")
async def auth_google_code(data: auth_request_schema.LoginGoogleCode, db: Session = Depends(get_db)):
    jwt_token = auth_service.auth_google_id_token(data.code, db)
    logger.info(f"📌 return jwt token - {jwt_token}")

    return {
        "jwt_token": jwt_token,
    }

@router.post("/login/google/id-token",
             description="구글 로그인시 발급되는 id-token을 사용하여 인증합니다.")
async def auth_google_token(data: auth_request_schema.LoginGoogleIdToken, db: Session = Depends(get_db)):
    jwt_token = auth_service.auth_google_id_token(data.id_token, db)
    logger.info(f"📌 return jwt token - {jwt_token}")

    return {
        "jwt_token": jwt_token,
    }

@router.post("/token/test",
             description="테스트용 access-token을 반환합니다.")
async def get_test_access_token(db: Session = Depends(get_db)):
    jwt_token = auth_service.make_test_access_token(db)
    return {
        "jwt_token": jwt_token,
    }

@router.get("/token",
            description="발급된 access-token에서 사용자 정보를 반환합니다.")
async def get_user_info_from_token(authorization: str = Depends(api_key_header)):
    try:
        payload = auth_service.decode_token(authorization)
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
    jwt_token = auth_service.auth_google_id_token(data.code, db)
    logger.info(f"📌 return jwt token - {jwt_token}")

    return {
        "jwt_token": jwt_token,
    }

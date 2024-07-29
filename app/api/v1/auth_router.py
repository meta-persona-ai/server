from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
import jwt

from ...db.database import get_db
from ...core.logger_config import setup_logger
from ...schemas.request import auth_request_schema
from ...schemas.response.auth_response_schema import ResponseToken, ResponseDecodeToken
from ...services import auth_service


logger = setup_logger()
api_key_header = APIKeyHeader(name="Authorization")

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"]
)


@router.post("/login/google/id-token",
             description="구글 로그인시 발급되는 id-token을 사용하여 인증합니다.",
             response_model=ResponseToken
             )
async def auth_google_token(data: auth_request_schema.LoginGoogleIdToken, db: Session = Depends(get_db)):
    jwt_token = auth_service.auth_google_id_token(data.id_token, db)
    logger.info(f"📌 return jwt token - {jwt_token}")

    return {
        "jwt_token": jwt_token,
    }

@router.post("/token/test",
             description="테스트용 access-token을 반환합니다.",
             response_model=ResponseToken
             )
async def get_test_access_token(db: Session = Depends(get_db)):
    jwt_token = auth_service.make_test_access_token(db)
    return {
        "jwt_token": jwt_token,
    }

@router.get("/token",
            description="발급된 access-token에서 사용자 정보를 반환합니다.",
            response_model=ResponseDecodeToken
            )
async def get_user_info_from_token(authorization: str = Depends(api_key_header)):
    try:
        payload = auth_service.decode_token(authorization)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


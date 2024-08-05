from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...db.database import get_db
from ...core import setup_logger, get_current_user
from ...schemas.request import auth_request_schema
from ...schemas.response.auth_response_schema import ResponseDecodeToken, LoginResponse
from ...services import AuthService

logger = setup_logger()

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"]
)

@router.post("/login/google/id-token",
             description="구글 로그인시 발급되는 id-token을 사용하여 인증합니다.",
             response_model=LoginResponse
             )
async def auth_google_token(data: auth_request_schema.LoginGoogleIdToken, db: Session = Depends(get_db)):
    response = AuthService.auth_google_id_token(data.id_token, db)
    logger.info(f"📌 return access token - {response['access_token']}")

    return response

@router.post("/token/test",
             description="테스트용 access-token을 반환합니다.",
             response_model=LoginResponse
             )
async def get_test_access_token(db: Session = Depends(get_db)):
    response = AuthService.make_test_access_token(db)
    return response

@router.get("/token",
            description="발급된 access-token에서 사용자 정보를 반환합니다.",
            response_model=ResponseDecodeToken
            )
async def get_user_info_from_token(user_id: str = Depends(get_current_user)):
    return {"user_id": user_id, "message": "This is a protected route"}


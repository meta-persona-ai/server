from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from ...database import get_db
from ...schemas.user_request_schema import User, UserUpdate
from ...services import user_service
from app.lib import jwt_util

router = APIRouter(
    prefix="/api/user",
    tags=["User"]
)

api_key_header = APIKeyHeader(name="Authorization")

@router.get("/",
            description="모든 유저를 조회합니다.",
            response_model=list[User]
            )
async def read_users(db: Session = Depends(get_db)):
    return user_service.get_users(db)

@router.get("/me",
            description="현재 로그인된 유저 정보를 조회합니다.",
            response_model=User
            )
async def read_current_user(authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    payload = jwt_util.decode_token(authorization)
    user = user_service.get_user_by_id(payload.id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/me",
               description="현재 로그인된 유저를 삭제합니다.",
               response_model=dict
               )
async def delete_current_user(authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    payload = jwt_util.decode_token(authorization)
    success = user_service.delete_user_by_id(payload.id, db)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@router.put("/me",
            description="현재 로그인된 유저 정보를 업데이트합니다.",
            response_model=User
            )
async def update_current_user(user_update: UserUpdate, authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    payload = jwt_util.decode_token(authorization)
    updated_user = user_service.update_user_by_id(payload.id, user_update, db)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.put("/me/deactivate",
            description="현재 로그인된 유저를 비활성화합니다.(탈퇴)",
            response_model=User
            )
async def deactivate_current_user(authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    payload = jwt_util.decode_token(authorization)
    deactivated_user = user_service.deactivate_user_by_id(payload.id, db)
    if not deactivated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return deactivated_user

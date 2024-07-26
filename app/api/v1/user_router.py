from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from ...db.database import get_db
from ...schemas.request.user_request_schema import UserUpdate
from ...schemas.response.user_response_schema import UserResponse, MessageResponse
from ...services import user_service
from app.utils import jwt_util

router = APIRouter(
    prefix="/api/v1/user",
    tags=["User"]
)

api_key_header = APIKeyHeader(name="Authorization")

@router.get("/",
            description="모든 유저를 조회합니다.",
            response_model=list[UserResponse]
            )
async def read_users(db: Session = Depends(get_db)):
    return user_service.get_users(db)

@router.get("/me",
            description="현재 로그인된 유저 정보를 조회합니다.",
            response_model=UserResponse
            )
async def read_current_user(authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    payload = jwt_util.decode_token(authorization)
    user = user_service.get_user_by_id(payload.id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/me",
               description="현재 로그인된 유저를 삭제합니다.",
               response_model=MessageResponse
               )
async def delete_current_user(authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    payload = jwt_util.decode_token(authorization)
    success = user_service.delete_user_by_id(payload.id, db)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"} if success else {"message": "User deletion failed"}

@router.put("/me",
            description="현재 로그인된 유저 정보를 업데이트합니다.",
            response_model=MessageResponse
            )
async def update_current_user(user_update: UserUpdate, authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    payload = jwt_util.decode_token(authorization)
    updated_user = user_service.update_user_by_id(payload.id, user_update, db)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated successfully"} if updated_user else {"message": "User update failed"}

@router.put("/me/deactivate",
            description="현재 로그인된 유저를 비활성화합니다.(탈퇴)",
            response_model=MessageResponse
            )
async def deactivate_current_user(authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    payload = jwt_util.decode_token(authorization)
    deactivated_user = user_service.deactivate_user_by_id(payload.id, db)
    if not deactivated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deactivated successfully"} if deactivated_user else {"message": "User deactivation failed"}

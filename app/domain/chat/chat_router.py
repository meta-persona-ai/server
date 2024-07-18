from fastapi import APIRouter, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.database import get_db
from app.lib import jwt_util
from app.schemas.chat_schema import ChatCreate
from . import chat_service


router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"]
)
api_key_header = APIKeyHeader(name="Authorization")

@router.post("/create",
            description="채팅방을 만듭니다.",
            )
async def create_chat(authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
    payload = jwt_util.decode_token(authorization)
    chat = ChatCreate(user_id=payload.id, character_id=1)
    return chat_service.create_chat(chat, db)

# @router.get("/",
#             description="모든 유저를 조회합니다.",
#             response_model=list[User]
#             )
# async def read_users(db: Session = Depends(get_db)):
#     return user_service.get_users(db)

# @router.get("/{user_id}",
#             description="유저 ID로 유저를 조회합니다.",
#             response_model=User
#             )
# async def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
#     user = user_service.get_user_by_id(user_id, db)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

# @router.get("/email/{user_email}",
#             description="유저 이메일로 유저를 조회합니다.",
#             response_model=User
#             )
# async def read_user_by_email(user_email: str, db: Session = Depends(get_db)):
#     user = user_service.get_user_by_email(user_email, db)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

# @router.delete("/{user_id}",
#                description="유저 ID로 유저를 삭제합니다.",
#                response_model=dict
#                )
# async def delete_user(user_id: int, db: Session = Depends(get_db)):
#     success = user_service.delete_user_by_id(user_id, db)
#     if not success:
#         raise HTTPException(status_code=404, detail="User not found")
#     return {"message": "User deleted successfully"}

# @router.put("/{user_id}",
#             description="유저 ID로 유저 정보를 업데이트합니다.",
#             response_model=User
#             )
# async def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
#     updated_user = user_service.update_user_by_id(user_id, user_update, db)
#     if not updated_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return updated_user

# @router.put("/deactivate/{user_id}",
#             description="유저 ID로 유저를 비활성화합니다.(탈퇴)",
#             response_model=User
#             )
# async def deactivate_user(user_id: int, db: Session = Depends(get_db)):
#     deactivated_user = user_service.deactivate_user_by_id(user_id, db)
#     if not deactivated_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return deactivated_user
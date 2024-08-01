from fastapi import APIRouter, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.response.default_image_response_schema import DefaultImageResposne
from app.services.default_image_service import DefaultImageService


router = APIRouter(
    prefix="/api/v1/default-images",
    tags=["default image"]
)
api_key_header = APIKeyHeader(name="Authorization")

# @router.post("/",
#             description="새 채팅방을 생성하는 API입니다.",
#             response_model=MessageResponse
#             )
# async def create_chat(character_id: int, authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
#     payload = jwt_util.verify_token(authorization)
#     character = character_service.get_characters_by_id(payload.id, db)
#     if not character:
#         raise HTTPException(status_code=404, detail="Character not found")
#     chat = ChatCreate(user_id=payload.id, character_id=character_id)
#     success = chat_service.create_chat(chat, db)
#     return {"message": "Chat created successfully"} if success else {"message": "Chat creation failed"}

@router.get("/",
            description="",
            response_model=list[DefaultImageResposne]
            )
async def get_default_images(db: Session = Depends(get_db)):
    return DefaultImageService.get_default_images(db)

# @router.delete("/{chat_id}",
#                description="특정 채팅방을 삭제하는 API입니다.",
#                response_model=MessageResponse
#                )
# async def delete_chat(chat_id: int, authorization: str = Depends(api_key_header), db: Session = Depends(get_db)):
#     payload = jwt_util.verify_token(authorization)
#     success = chat_service.delete_chat_by_id(chat_id, payload.id, db)
#     return {"message": "Chat deleted successfully"} if success else {"message": "Chat deletion failed"}

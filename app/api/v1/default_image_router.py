from fastapi import APIRouter, Depends, UploadFile, Form, File
from sqlalchemy.orm import Session

from ...db.database import get_db
from ...schemas.response.default_image_response_schema import DefaultImageResposne, MessageResponse
from ...services.default_image_service import DefaultImageService


router = APIRouter(
    prefix="/api/v1/default-images",
    tags=["default image"]
)

@router.post("/",
            description="기본 이미지을 저장하는 API입니다.",
            response_model=MessageResponse
            )
async def create_default_image(
    name: str = Form(...), 
    image: UploadFile = File(...), 
    db: Session = Depends(get_db)
):  
    await DefaultImageService.create_image(name, image, db)

    return {"message": "Chat created successfully"} if True else {"message": "Chat creation failed"}

@router.get("/",
            description="기본 이미지를 불러오는 API입니다.",
            response_model=list[DefaultImageResposne]
            )
async def get_default_images(db: Session = Depends(get_db)):
    return DefaultImageService.get_default_images(db)

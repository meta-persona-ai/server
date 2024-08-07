from fastapi import APIRouter, Depends, UploadFile, Form, File
from sqlalchemy.orm import Session

from ...db.database import get_db
from ...schemas.response.default_image_response_schema import DefaultImageResposne, MessageResponse
from ...services.default_image_service import DefaultImageService
from ...schemas.request.default_image_request_schema import DefaultImageCreate


router = APIRouter(
    prefix="/api/v1/default-images",
    tags=["Default image"]
)

@router.post("/",
            description="기본 이미지을 저장하는 API입니다.",
            response_model=MessageResponse
            )
async def create_default_image(
    name: str = Form(...), 
    gender: str = Form(...), 
    age_group: str = Form(...), 
    image: UploadFile = File(...), 
    db: Session = Depends(get_db)
):  
    image_data = DefaultImageCreate(
        image_name=name, 
        image_gender=gender,
        image_age_group=age_group
        )
    await DefaultImageService.create_image(image_data, image, db)

    return {"message": "Image created successfully"} if True else {"message": "Image creation failed"}

@router.get("/",
            description="기본 이미지를 불러오는 API입니다.",
            response_model=list[DefaultImageResposne]
            )
async def get_default_images(db: Session = Depends(get_db)):
    return DefaultImageService.get_default_images(db)

from fastapi import UploadFile
from sqlalchemy.orm import Session

from ..crud import default_image_crud
from ..schemas.request.default_image_request_schema import DefaultImageCreate, DefaultImageUpdate
from ..utils.s3_util import upload_to_s3

class DefaultImageService:
    @staticmethod    
    async def create_image(image_name: str, image_file: UploadFile, db: Session):
        image_url = await upload_to_s3(image_file)
        image = DefaultImageCreate(image_name=image_name, image_url=image_url)
        return default_image_crud.create_image(image, db)

    @staticmethod
    def get_default_images(db: Session):
        return default_image_crud.get_default_images(db)

    @staticmethod
    def get_default_images_by_id(image_id: int, db: Session):
        return default_image_crud.get_default_images_by_id(image_id, db)

    @staticmethod
    def update_default_image(image_id: int, relationship_update: DefaultImageUpdate, db: Session):
        return default_image_crud.update_default_image(image_id, relationship_update, db)

    @staticmethod
    def delete_default_image(image_id: int, db: Session):
        return default_image_crud.delete_default_image(image_id, db)

from sqlalchemy.orm import Session

from ..crud import default_image_crud
from ..schemas.request.default_image_request_schema import DefaultImageCreate, DefaultImageUpdate

class DefaultImageService:
    @staticmethod
    def create_image(image: DefaultImageCreate, db: Session):
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

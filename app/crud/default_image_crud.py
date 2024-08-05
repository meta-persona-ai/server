from sqlalchemy.orm import Session
from ..models.default_images import DefaultImages
from ..schemas.request.default_image_request_schema import DefaultImageCreate, DefaultImageUpdate


# Create
def create_image(image: DefaultImageCreate, db: Session):
    db_default_image = DefaultImages(
        image_name = image.image_name,
        image_url = image.image_url,
        image_gender = image.image_gender,
        image_age_group = image.image_age_group
    )
    db.add(db_default_image)
    db.commit()
    db.refresh(db_default_image)
    return db_default_image

# Read
def get_default_images(db: Session) -> list[DefaultImages]:
    return db.query(DefaultImages).all()

def get_default_images_by_id(image_id: int, db: Session) -> DefaultImages:
    return db.query(DefaultImages).filter(DefaultImages.image_id == image_id).first()

def get_default_images_by_name(image_name: int, db: Session) -> DefaultImages:
    return db.query(DefaultImages).filter(DefaultImages.image_name == image_name).first()

# Update
def update_default_image(image_id: int, image_update: DefaultImageUpdate, db: Session):
    db_default_image = get_default_images_by_id(image_id, db)
    if db_default_image:
        for attr, value in vars(image_update).items():
            if value is not None and attr != "_sa_instance_state":
                setattr(db_default_image, attr, value)
        db.commit()
        return db_default_image
    return None

# Delete
def delete_default_image(image_id: int, db: Session) -> bool:
    db_relationship = get_default_images_by_id(image_id, db)
    if db_relationship:
        db.delete(db_relationship)
        db.commit()
        return True
    return False

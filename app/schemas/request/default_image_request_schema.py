from fastapi_camelcase import CamelModel

from app.models import ImageAgeGroupEnum, ImageGenderEnum

class DefaultImageCreate(CamelModel):
    image_name: str
    image_url: str | None = None
    image_gender: ImageGenderEnum | None = None
    image_age_group: ImageAgeGroupEnum | None = None

class DefaultImageUpdate(CamelModel):
    image_name: str | None = None
    image_url: str | None = None
    image_gender: ImageGenderEnum | None = None
    image_age_group: ImageAgeGroupEnum | None = None


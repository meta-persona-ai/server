from fastapi_camelcase import CamelModel


class DefaultImageCreate(CamelModel):
    image_name: str
    image_url: str

class DefaultImageUpdate(CamelModel):
    image_name: str
    image_url: str


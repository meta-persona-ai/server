from fastapi_camelcase import CamelModel


class DefaultImageResposne(CamelModel):
    image_id: int
    image_name: str
    image_url: str

from fastapi_camelcase import CamelModel


class DefaultImageResposne(CamelModel):
    image_id: int
    image_name: str
    image_url: str
    image_gender: str | None = None
    image_age_group: str | None = None

class MessageResponse(CamelModel):
    message: str
from fastapi_camelcase import CamelModel


class ResponseToken(CamelModel):
    jwt_token: str

class ResponseDecodeToken(CamelModel):
    id: int
    email: str
    name: str
    picture: str | None = None

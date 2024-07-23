from pydantic import BaseModel
from fastapi_camelcase import CamelModel


class LoginGoogleCode(BaseModel):
    code: str

class LoginGoogleToken(BaseModel):
    token: str

class LoginGoogleIdToken(CamelModel):
    id_token: str

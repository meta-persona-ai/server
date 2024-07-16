from pydantic import BaseModel


class LoginGoogleCode(BaseModel):
    code: str

class LoginGoogleToken(BaseModel):
    token: str

from pydantic import BaseModel


class AuthMessage(BaseModel):
    type: str
    token: str

class UserMessage(BaseModel):
    type: str
    message: str

class SystemMessage(BaseModel):
    type: str
    message: str

class CharacterMessage(BaseModel):
    type: str
    character_name: str
    response_id: int
    character: str
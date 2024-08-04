from pydantic import BaseModel


class AuthMessage(BaseModel):
    type: str
    token: str

class UserMessage(BaseModel):
    type: str
    content: str

class SystemMessage(BaseModel):
    type: str
    characterName: str
    responseId: int
    message: str

class CharacterMessage(BaseModel):
    type: str
    characterName: str
    responseId: int
    streamContent: str
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt

from database import get_db
from . import auth_service

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/login/google")
async def login_google():
    login_url = auth_service.login_google()
    return {
        "url": login_url
    }

@router.get("/google")
async def auth_google(code: str, db: Session = Depends(get_db)):
    jwt_token = auth_service.auth_google(code, db)
    return {
        "jwt_token": jwt_token,
    }

@router.get("/token")
async def get_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = auth_service.decode_token(token)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

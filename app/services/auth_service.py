from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..core.logger_config import setup_logger
from ..utils import google_api
from ..utils import jwt_util
from ..crud import auth_crud
from ..services import user_service
from ..schemas.request.user_request_schema import UserCreate
from ..schemas.schemas import UserSchema


logger = setup_logger()


def auth_google_id_token(id_token: str, db: Session):
    user = google_api.decode_id_token(id_token)
    if not user:
        raise HTTPException(status_code=401, detail="id token is not valid")

    existing_user = user_service.get_user_by_email(user.user_email, db)
    if existing_user:
        db_user = existing_user
        status = "success"
        message = "Login successful."
    else:
        db_user = auth_crud.create_user(user, db)
        status = "registration"
        message = "User not found. Please complete the registration process."
        logger.info(f"📌 successfully sign in - id: {db_user.user_id}, name: {db_user.user_name}, email: {db_user.user_email}")

    logger.info(f"📌 login complete! - id: {db_user.user_id}, name: {db_user.user_name}")

    response = {
        "status": status,
        "message": message,
        "user": db_user,
        "access_token": jwt_util.make_access_token(db_user)
    }
    return response


def make_test_access_token(db: Session):
    test_email = "test@example.com"

    existing_user = user_service.get_user_by_email(test_email, db)

    if existing_user:
        db_user = existing_user
        status = "success"
        message = "Login successful."
    else:
        test_user = UserCreate(user_email=test_email, user_password="test", user_name="Test User", user_profile="test.jpg")
        db_user = auth_crud.create_user(test_user, db)
        status = "registration"
        message = "User not found. Please complete the registration process."

    response = {
        "status": status,
        "message": message,
        "user": db_user,
        "access_token": jwt_util.make_access_token(db_user)
    }
    return response


def decode_token(authorization: str) -> UserSchema:
    return jwt_util.decode_token(authorization)
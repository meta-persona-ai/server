from sqlalchemy.orm import Session

from . import database
from ..schemas import user_schema
from ..crud import auth_crud, user_crud

def init_db():
    db = Session(bind=database.engine)

    make_init_user(db)

    db.close()

def make_init_user(db: Session):
    test_email = "test@example.com"
    existing_user = user_crud.get_user_by_email(test_email, db)
    if not existing_user:
        test_user = user_schema.UserCreate(user_email=test_email, user_password="test", user_name="Test User", user_profile="test.jpg")
        auth_crud.create_user(test_user, db)
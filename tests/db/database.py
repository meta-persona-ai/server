from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pytest

from app.db.database import Base
from app.db.initial_data import DatabaseInitializer

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    initializer = DatabaseInitializer(engine)
    initializer.init_db()

    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from sqlalchemy.ext.declarative import declarative_base
import pytest

from app.main import app  # FastAPI 앱을 import합니다.
from app.database import Base, get_db
from app.models.user_model import User

# 테스트 데이터베이스를 설정합니다.
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 테스트용 데이터베이스를 초기화합니다.
Base.metadata.create_all(bind=engine)

# FastAPI 앱에 대한 테스트 클라이언트를 설정합니다.
client = TestClient(app)

# 테스트용 데이터베이스 세션을 반환하는 종속성을 정의합니다.
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# 테스트 전에 테스트 데이터베이스를 초기화하고 데이터를 추가합니다.
@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    user = User(email="test@example.com", hashed_password="test", name="Test User")
    db.add(user)
    db.commit()
    db.refresh(user)
    
    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_read_user(db_session: Session):
    response = client.get(f"/api/user/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["email"] == "test@example.com"


def test_read_user_by_id(db_session: Session):
    user_id = db_session.query(User).filter(User.email == "test@example.com").first().id
    response = client.get(f"/api/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"


def test_read_user_by_email(db_session: Session):
    response = client.get("/api/user/email/test@example.com")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"

def test_update_user(db_session: Session):
    user_id = db_session.query(User).filter(User.email == "test@example.com").first().id
    response = client.put(
        f"/api/user/{user_id}",
        json={"name": "Updated User"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated User"


def test_deactivate_user(db_session: Session):
    user_id = db_session.query(User).filter(User.email == "test@example.com").first().id
    response = client.put(f"/api/user/deactivate/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["is_active"] == False

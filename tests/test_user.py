from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.database import Base, get_db
from app.models.user import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

client = TestClient(app)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    user = User(user_email="test@example.com", user_password="test", user_name="Test User", user_profile="test.jpg")
    db.add(user)
    db.commit()
    db.refresh(user)
    
    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_read_users(db_session: Session):
    response = client.get(f"/api/user/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["user_email"] == "test@example.com"


def test_read_current_user(db_session: Session):
    response = client.post("/api/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwt_token")

    headers = {"Authorization": f"Bearer {test_token}"}

    response = client.get(f"/api/user/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["user_name"] == "Test User"
    assert data["user_email"] == "test@example.com"


def test_update_current_user(db_session: Session):
    response = client.post("/api/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwt_token")

    headers = {"Authorization": f"Bearer {test_token}"}

    response = client.put(
        f"/api/user/me",
        json={"user_name": "Updated User"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user_name"] == "Updated User"


def test_deactivate_user(db_session: Session):
    response = client.post("/api/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwt_token")

    headers = {"Authorization": f"Bearer {test_token}"}

    response = client.put(f"/api/user/me/deactivate", headers=headers)
    assert response.status_code == 200

    test_user = db_session.query(User).filter(User.user_email == "test@example.com").first()
    db_session.refresh(test_user)
    assert test_user.user_is_active == False

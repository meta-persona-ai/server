from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.db.database import Base, get_db
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
    """
    모든 사용자 조회 테스트.
    이 테스트는 /api/user/ 엔드포인트를 호출하여 모든 사용자를 조회하는지 확인합니다.
    """
    response = client.get(f"/api/v1/user/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["userEmail"] == "test@example.com"

def test_read_current_user(db_session: Session):
    """
    현재 로그인한 사용자 정보 조회 테스트.
    이 테스트는 /api/user/me 엔드포인트를 호출하여 현재 로그인한 사용자의 정보를 조회하는지 확인합니다.
    """
    response = client.post("/api/v1/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwtToken")

    headers = {"Authorization": f"Bearer {test_token}"}

    response = client.get(f"/api/v1/user/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["userName"] == "Test User"
    assert data["userEmail"] == "test@example.com"

def test_update_current_user(db_session: Session):
    """
    현재 로그인한 사용자 정보 업데이트 테스트.
    이 테스트는 /api/user/me 엔드포인트를 호출하여 현재 로그인한 사용자의 정보를 업데이트하는지 확인합니다.
    """
    response = client.post("/api/v1/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwtToken")

    headers = {"Authorization": f"Bearer {test_token}"}

    response = client.put(
        f"/api/v1/user/me",
        json={"userName": "Updated User"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User updated successfully"

def test_deactivate_user(db_session: Session):
    """
    사용자 비활성화 테스트.
    이 테스트는 /api/user/me/deactivate 엔드포인트를 호출하여 현재 로그인한 사용자를 비활성화하는지 확인합니다.
    """
    response = client.post("/api/v1/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwtToken")

    headers = {"Authorization": f"Bearer {test_token}"}

    response = client.put(f"/api/v1/user/me/deactivate", headers=headers)
    assert response.status_code == 200

    test_user = db_session.query(User).filter(User.user_email == "test@example.com").first()
    db_session.refresh(test_user)
    assert test_user.user_is_active == False

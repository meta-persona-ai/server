from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.db.database import Base, get_db

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
    
    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_get_test_token(db_session: Session):
    """
    테스트용 토큰 생성 테스트.
    이 테스트는 /api/auth/token/test 엔드포인트를 호출하여 JWT 토큰을 생성하는지 확인합니다.
    """
    response = client.post("/api/auth/token/test")
    assert response.status_code == 200
    assert "jwt_token" in response.json()

def test_google_login_url(db_session: Session):
    """
    구글 로그인 URL 테스트.
    이 테스트는 /api/auth/login/google 엔드포인트를 호출하여 구글 로그인 URL을 가져오는지 확인합니다.
    """
    response = client.get("/api/auth/login/google")
    assert response.status_code == 200
    assert "url" in response.json()

def test_get_user_info_from_token(db_session: Session):
    """
    토큰으로부터 사용자 정보 가져오기 테스트.
    이 테스트는 /api/auth/token 엔드포인트를 호출하여 JWT 토큰으로부터 사용자 정보를 가져오는지 확인합니다.
    """
    response = client.post("/api/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwt_token")

    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/auth/token", headers=headers)
    assert response.status_code == 200
    assert "email" in response.json()
    assert "id" in response.json()
    assert "name" in response.json()

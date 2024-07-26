from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.main import app
from app.db.database import get_db

from tests.db.database import override_get_db, db_session


client = TestClient(app)
app.dependency_overrides[get_db] = override_get_db


def test_get_test_token(db_session: Session):
    """
    테스트용 토큰 생성 테스트.
    이 테스트는 /api/auth/token/test 엔드포인트를 호출하여 JWT 토큰을 생성하는지 확인합니다.
    """
    response = client.post("/api/v1/auth/token/test")
    assert response.status_code == 200
    assert "jwtToken" in response.json()

def test_google_login_url(db_session: Session):
    """
    구글 로그인 URL 테스트.
    이 테스트는 /api/auth/login/google 엔드포인트를 호출하여 구글 로그인 URL을 가져오는지 확인합니다.
    """
    response = client.get("/api/v1/auth/login/google")
    assert response.status_code == 200
    assert "url" in response.json()

def test_get_user_info_from_token(db_session: Session):
    """
    토큰으로부터 사용자 정보 가져오기 테스트.
    이 테스트는 /api/auth/token 엔드포인트를 호출하여 JWT 토큰으로부터 사용자 정보를 가져오는지 확인합니다.
    """
    response = client.post("/api/v1/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwtToken")

    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/v1/auth/token", headers=headers)
    assert response.status_code == 200
    assert "email" in response.json()
    assert "id" in response.json()
    assert "name" in response.json()

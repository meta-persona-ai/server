from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session
from app.models.user import User

from tests.get_token import get_token

@pytest.fixture
def client(client: TestClient) -> TestClient:
    return client

def test_read_users(client: TestClient):
    """
    모든 사용자 조회 테스트.
    이 테스트는 /api/user/ 엔드포인트를 호출하여 모든 사용자를 조회하는지 확인합니다.
    """
    response = client.get(f"/api/v1/user/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["userEmail"] == "test@example.com"

def test_read_current_user(client: TestClient):
    """
    현재 로그인한 사용자 정보 조회 테스트.
    이 테스트는 /api/user/me 엔드포인트를 호출하여 현재 로그인한 사용자의 정보를 조회하는지 확인합니다.
    """
    headers = get_token(client)

    response = client.get(f"/api/v1/user/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["userName"] == "Test User"
    assert data["userEmail"] == "test@example.com"

def test_update_current_user(client: TestClient):
    """
    현재 로그인한 사용자 정보 업데이트 테스트.
    이 테스트는 /api/user/me 엔드포인트를 호출하여 현재 로그인한 사용자의 정보를 업데이트하는지 확인합니다.
    """
    headers = get_token(client)

    response = client.put(
        f"/api/v1/user/me",
        json={"userName": "Updated User"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User updated successfully"

def test_update_current_user2(client: TestClient, db_session: Session):
    headers = get_token(client)

    gender = "other"
    birthdate = "1990-01-01T00:00:00"

    response = client.put(
        f"/api/v1/user/me",
        json={"userGender": gender, "userBirthdate": birthdate},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User updated successfully"

    response = client.get(f"/api/v1/user/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['userGender'] == gender
    assert data['userBirthdate'] == birthdate

def test_deactivate_user(client: TestClient, db_session: Session):
    """
    사용자 비활성화 테스트.
    이 테스트는 /api/user/me/deactivate 엔드포인트를 호출하여 현재 로그인한 사용자를 비활성화하는지 확인합니다.
    """
    headers = get_token(client)

    response = client.put(f"/api/v1/user/me/deactivate", headers=headers)
    assert response.status_code == 200

    test_user = db_session.query(User).filter(User.user_email == "test@example.com").first()
    db_session.refresh(test_user)
    assert test_user.user_is_active == False

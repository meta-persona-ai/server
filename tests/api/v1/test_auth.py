from fastapi.testclient import TestClient
import pytest

@pytest.fixture
def client(client):
    return client

def test_get_test_token(client: TestClient):
    """
    테스트용 토큰 생성 테스트.
    이 테스트는 /api/v1/auth/token/test 엔드포인트를 호출하여 JWT 토큰을 생성하는지 확인합니다.
    """
    response = client.post("/api/v1/auth/token/test")
    assert response.status_code == 200
    assert "accessToken" in response.json()

def test_get_user_info_from_token(client: TestClient):
    """
    토큰으로부터 사용자 정보 가져오기 테스트.
    이 테스트는 /api/v1/auth/token 엔드포인트를 호출하여 JWT 토큰으로부터 사용자 정보를 가져오는지 확인합니다.
    """
    response = client.post("/api/v1/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("accessToken")

    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/v1/auth/token", headers=headers)

    assert response.status_code == 200
    assert "userId" in response.json()
    assert "message" in response.json()

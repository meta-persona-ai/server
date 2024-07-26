from fastapi.testclient import TestClient
import pytest

@pytest.fixture
def client(client: TestClient) -> TestClient:
    return client

def test_get_my_chat(client: TestClient):
    """
    현재 사용자의 채팅 및 채팅 로그 조회 테스트.
    이 테스트는 /api/v1/chat/me 엔드포인트와 /api/v1/chat-log/me/{chatId} 엔드포인트를 호출하여 
    현재 로그인한 사용자의 채팅과 해당 채팅의 로그를 조회하는지 확인합니다.
    """
    response = client.post("/api/v1/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwtToken")

    headers = {"Authorization": f"Bearer {test_token}"}
    
    response = client.get(f"/api/v1/chat/me", headers=headers)
    assert response.status_code == 200
    data = response.json()

    response = client.get(f"/api/v1/chat-log/me/{data[0]['chatId']}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_delete_chat(client: TestClient):
    """
    채팅 로그 삭제 테스트.
    이 테스트는 /api/v1/chat-log/{chatId} 엔드포인트를 호출하여 특정 채팅 로그를 삭제하는지 확인합니다.
    """
    response = client.post("/api/v1/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwtToken")

    headers = {"Authorization": f"Bearer {test_token}"}

    response = client.get(f"/api/v1/chat/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    chat_id = data[0]['chatId']

    response = client.get(f"/api/v1/chat-log/me/{chat_id}", headers=headers)
    assert response.status_code == 200
    before = len(response.json())

    response = client.delete(f"/api/v1/chat-log/{chat_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Log deleted successfully'

    response = client.get(f"/api/v1/chat-log/me/{chat_id}", headers=headers)
    assert response.status_code == 200
    after = len(response.json())

    assert before == after + 1

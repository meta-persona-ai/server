from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session
from app.models.character import Character
from app.models.chat import Chat

@pytest.fixture
def client(client: TestClient) -> TestClient:
    return client

def test_create_chat(client: TestClient, db_session: Session):
    """
    새로운 채팅 생성 테스트.
    이 테스트는 /api/v1/chat 엔드포인트를 호출하여 새로운 채팅을 생성하는지 확인합니다.
    """
    response = client.post("/api/v1/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwtToken")

    headers = {"Authorization": f"Bearer {test_token}"}
    test_character = db_session.query(Character).first()
    
    response = client.post(f"/api/v1/chat?character_id={test_character.character_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Chat created successfully"

def test_get_my_chats(client: TestClient):
    """
    현재 사용자의 모든 채팅 조회 테스트.
    이 테스트는 /api/v1/chat/me 엔드포인트를 호출하여 현재 로그인한 사용자의 모든 채팅을 조회하는지 확인합니다.
    """
    response = client.post("/api/v1/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwtToken")

    headers = {"Authorization": f"Bearer {test_token}"}
    
    response = client.get(f"/api/v1/chat/me/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_delete_chat(client: TestClient, db_session: Session):
    """
    채팅 삭제 테스트.
    이 테스트는 /api/v1/chat/{character_id} 엔드포인트를 호출하여 특정 채팅을 삭제하는지 확인합니다.
    """
    response = client.post("/api/v1/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwtToken")

    headers = {"Authorization": f"Bearer {test_token}"}

    user_info = client.get("/api/v1/auth/token", headers=headers).json()

    test_chat = db_session.query(Chat).filter(Chat.user_id == user_info['id']).first()
    
    response = client.delete(f"/api/v1/chat/{test_chat.character_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Chat deleted successfully'

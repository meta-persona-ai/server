from fastapi.testclient import TestClient
import pytest

@pytest.fixture
def client(client: TestClient) -> TestClient:
    return client


def test_get_my_chat(client: TestClient):
    response = client.post("/api/v1/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwtToken")

    headers = {"Authorization": f"Bearer {test_token}"}
    
    response = client.get(f"/api/v1/chat/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    print(data[0])

    # response = client.get(f"/api/v1/chat-log/me/{chat_id}", headers=headers)
    # assert response.status_code == 200
    # data = response.json()
    # assert len(data) > 0
    assert False

# def test_delete_chat(client: TestClient, db_session: Session):
#     response = client.post("/api/v1/auth/token/test")
#     assert response.status_code == 200
#     test_token = response.json().get("jwtToken")

#     headers = {"Authorization": f"Bearer {test_token}"}

#     user_info = client.get("/api/v1/auth/token", headers=headers).json()

#     test_chat = db_session.query(Chat).filter(Chat.user_id == user_info['id']).first()
    
#     response = client.delete(f"/api/v1/chat/{test_chat.character_id}", headers=headers)
#     assert response.status_code == 200
#     data = response.json()
#     assert data['message'] == 'Chat deleted successfully'

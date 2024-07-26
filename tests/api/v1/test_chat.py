from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.main import app
from app.db.database import get_db
from app.models.character import Character
from app.models.chat import Chat

from tests.db.database import override_get_db, db_session


client = TestClient(app)
app.dependency_overrides[get_db] = override_get_db


def test_create_chat(db_session: Session):
    response = client.post("/api/v1/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwtToken")

    headers = {"Authorization": f"Bearer {test_token}"}
    test_character = db_session.query(Character).first()
    
    response = client.post(f"/api/v1/chat?character_id={test_character.character_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Chat created successfully"

def test_get_my_chat(db_session: Session):
    response = client.post("/api/v1/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwtToken")

    headers = {"Authorization": f"Bearer {test_token}"}
    
    response = client.get(f"/api/v1/chat/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_delete_chat(db_session: Session):
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

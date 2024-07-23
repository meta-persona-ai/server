from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.db.initial_data import DatabaseInitializer
from app.db.database import Base, get_db
from app.models.character import Character
from app.models.chat import Chat

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
    
    initializer = DatabaseInitializer(engine)
    initializer.init_db()

    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_chat(db_session: Session):
    response = client.post("/api/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwtToken")

    headers = {"Authorization": f"Bearer {test_token}"}
    test_character = db_session.query(Character).first()
    
    response = client.post(f"/api/chat?character_id={test_character.character_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Chat created successfully"

def test_get_my_chat(db_session: Session):
    response = client.post("/api/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwtToken")

    headers = {"Authorization": f"Bearer {test_token}"}
    
    response = client.get(f"/api/chat/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_delete_chat(db_session: Session):
    response = client.post("/api/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwtToken")

    headers = {"Authorization": f"Bearer {test_token}"}

    user_info = client.get("/api/auth/token", headers=headers).json()

    test_chat = db_session.query(Chat).filter(Chat.user_id == user_info['id']).first()
    
    response = client.delete(f"/api/chat/{test_chat.character_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Chat deleted successfully'

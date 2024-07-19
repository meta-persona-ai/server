from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.db.database import Base, get_db
from app.models.character import Character

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

    exam_character = {
        "character_details": "Test details",
        "character_gender": "male",
        "character_name": "test",
        "character_personality": "Test personality",
        "character_profile": "Test profile",
        "user_id": 1
    }

    character = Character(**exam_character)
    db.add(character)
    db.commit()
    db.refresh(character)
    
    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_chat(db_session: Session):
    response = client.post("/api/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwt_token")

    headers = {"Authorization": f"Bearer {test_token}"}
    test_character = db_session.query(Character).first()
    
    response = client.post(f"/api/chat?character_id={test_character.character_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert False
    # data = response.json()
    # test_character = db_session.query(Character).filter(Character.character_id == data['character_id']).first()
    # assert test_character.character_name == exam_character.get('character_name')

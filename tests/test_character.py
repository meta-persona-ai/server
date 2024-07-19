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
    
    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_character(db_session: Session):
    """
    캐릭터 생성 테스트.
    이 테스트는 /api/characters 엔드포인트를 호출하여 새로운 캐릭터를 생성하는지 확인합니다.
    """
    response = client.post("/api/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwt_token")

    headers = {"Authorization": f"Bearer {test_token}"}

    exam_character = {
        "character_details": "Test details",
        "character_gender": "male",
        "character_name": "test",
        "character_personality": "Test personality",
        "character_profile": "Test profile"
    }
    
    response = client.post("/api/characters", json=exam_character, headers=headers)
    assert response.status_code == 200
    data = response.json()
    test_character = db_session.query(Character).filter(Character.character_id == data['character_id']).first()
    assert test_character.character_name == exam_character.get('character_name')

def test_get_all_characters(db_session: Session):
    """
    모든 캐릭터 조회 테스트.
    이 테스트는 /api/characters 엔드포인트를 호출하여 모든 캐릭터 정보를 조회하는지 확인합니다.
    """
    response = client.get("/api/characters/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["character_name"] == "test"

def test_get_my_characters(db_session: Session):
    """
    로그인한 사용자의 캐릭터 조회 테스트.
    이 테스트는 /api/characters/me 엔드포인트를 호출하여 로그인한 사용자의 캐릭터를 조회하는지 확인합니다.
    """
    response = client.post("/api/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwt_token")

    headers = {"Authorization": f"Bearer {test_token}"}
    
    response = client.get("/api/characters/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data[0]["character_name"] == "test"

def test_update_character(db_session: Session):
    """
    캐릭터 업데이트 테스트.
    이 테스트는 /api/characters 엔드포인트를 호출하여 기존 캐릭터 정보를 업데이트하는지 확인합니다.
    """
    response = client.post("/api/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwt_token")

    headers = {"Authorization": f"Bearer {test_token}"}
    
    response = client.put(
        "/api/characters/1", 
        json={"character_name": "Updated Character"},
        headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["character_name"] == "Updated Character"

def test_delete_character(db_session: Session):
    """
    캐릭터 삭제 테스트.
    이 테스트는 /api/characters 엔드포인트를 호출하여 기존 캐릭터를 삭제하는지 확인합니다.
    """
    response = client.post("/api/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwt_token")

    headers = {"Authorization": f"Bearer {test_token}"}
    
    response = client.delete("/api/characters/1", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Character deleted successfully"

from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.main import app
from app.db.database import get_db

from tests.db.database import override_get_db, db_session


client = TestClient(app)
app.dependency_overrides[get_db] = override_get_db


def test_create_character(db_session: Session):
    """
    캐릭터 생성 테스트.
    이 테스트는 /api/characters 엔드포인트를 호출하여 새로운 캐릭터를 생성하는지 확인합니다.
    """
    response = client.post("/api/v1/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwtToken")

    headers = {"Authorization": f"Bearer {test_token}"}

    exam_character = {
        "characterDetails": "Test details",
        "characterGender": "male",
        "characterName": "test",
        "characterPersonality": "Test personality",
        "characterProfile": "Test profile"
    }
    
    response = client.post("/api/v1/characters", json=exam_character, headers=headers)
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data['message'] == 'Character created successfully'

def test_get_all_characters(db_session: Session):
    """
    모든 캐릭터 조회 테스트.
    이 테스트는 /api/characters 엔드포인트를 호출하여 모든 캐릭터 정보를 조회하는지 확인합니다.
    """
    response = client.get("/api/v1/characters/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["characterName"] == "init charater"

def test_get_my_characters(db_session: Session):
    """
    로그인한 사용자의 캐릭터 조회 테스트.
    이 테스트는 /api/characters/me 엔드포인트를 호출하여 로그인한 사용자의 캐릭터를 조회하는지 확인합니다.
    """
    response = client.post("/api/v1/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwtToken")

    headers = {"Authorization": f"Bearer {test_token}"}
    
    response = client.get("/api/v1/characters/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data[0]["characterName"] == "init charater"

def test_update_character(db_session: Session):
    """
    캐릭터 업데이트 테스트.
    이 테스트는 /api/characters 엔드포인트를 호출하여 기존 캐릭터 정보를 업데이트하는지 확인합니다.
    """
    response = client.post("/api/v1/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwtToken")

    headers = {"Authorization": f"Bearer {test_token}"}
    
    response = client.put(
        "/api/v1/characters/1", 
        json={"characterName": "Updated Character"},
        headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Character updated successfully"

# def test_delete_character(db_session: Session):
#     """
#     캐릭터 삭제 테스트.
#     이 테스트는 /api/characters 엔드포인트를 호출하여 기존 캐릭터를 삭제하는지 확인합니다.
#     """
#     response = client.post("/api/v1/auth/token/test")
#     assert response.status_code == 200
#     test_token = response.json().get("jwtToken")

#     headers = {"Authorization": f"Bearer {test_token}"}
    
#     response = client.delete("/api/v1/characters/1", headers=headers)
#     assert response.status_code == 200
#     data = response.json()
#     assert data["message"] == "Character deleted successfully"

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest

from app.models.characters import Character

from tests.get_token import get_token

@pytest.fixture
def client(client: TestClient) -> TestClient:
    return client

def test_create_character(client: TestClient):
    """
    캐릭터 생성 테스트.
    이 테스트는 /api/characters 엔드포인트를 호출하여 새로운 캐릭터를 생성하는지 확인합니다.
    """
    headers = get_token(client)

    exam_character = {
        "characterName": "test",
        "characterProfile": "Test profile",
        "characterGender": "male",
        "characterPersonality": "Test personality",
        "characterDetails": "Test details",
        "characterIsPublic": True,
        "relationships": [1,2]
    }
    
    response = client.post("/api/v1/characters", json=exam_character, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Character created successfully'
    character_id = data['characterId']

    response = client.get(f"/api/v1/characters/{character_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()

    assert [r['relationship']['relationshipId'] for r in data['characterRelationships']] == [1,2]


def test_get_all_characters(client: TestClient):
    """
    모든 캐릭터 조회 테스트.
    이 테스트는 /api/characters 엔드포인트를 호출하여 모든 캐릭터 정보를 조회하는지 확인합니다.
    """
    response = client.get("/api/v1/characters/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_get_character(client):
    headers = get_token(client)

    response = client.get("/api/v1/characters/")
    assert response.status_code == 200
    character_id = response.json()[0]['characterId']

    response = client.get(f"/api/v1/characters/{character_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['characterId'] == character_id

def test_get_my_characters(client: TestClient):
    """
    로그인한 사용자의 캐릭터 조회 테스트.
    이 테스트는 /api/characters/me 엔드포인트를 호출하여 로그인한 사용자의 캐릭터를 조회하는지 확인합니다.
    """
    headers = get_token(client)
    
    response = client.get("/api/v1/characters/me/", headers=headers)
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_update_character(client: TestClient):
    """
    캐릭터 업데이트 테스트.
    이 테스트는 /api/characters 엔드포인트를 호출하여 기존 캐릭터 정보를 업데이트하는지 확인합니다.
    """
    headers = get_token(client)
    
    response = client.put(
        "/api/v1/characters/1", 
        json={"characterName": "Updated Character"},
        headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Character updated successfully"

def test_update_character_is_public(client: TestClient, db_session: Session):
    headers = get_token(client)

    response = client.get("/api/v1/characters/me/", headers=headers)
    assert response.status_code == 200
    character_id = response.json()[-1]['characterId']

    updata_data = {
        "characterName": "Updated Character",
        "characterDetails": "Updata characterIsPublic",
        "characterIsPublic": False
    }
    
    response = client.put(
        f"/api/v1/characters/{character_id}", 
        json=updata_data,
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Character updated successfully"

    response = client.get("/api/v1/characters/")
    assert response.status_code == 200
    data = response.json()
    character_list = [character.get("characterId") for character in data]
    assert character_id not in character_list

    updated_character = db_session.query(Character).filter(Character.character_id == character_id).first()
    assert updated_character.character_is_public == False

def test_update_character_usage_count(client: TestClient, db_session: Session):
    headers = get_token(client)

    response = client.get("/api/v1/characters/me/", headers=headers)
    assert response.status_code == 200
    character_id = response.json()[0]['characterId']

    before_count = db_session.query(Character).filter(Character.character_id == character_id).first().character_usage_count

    response = client.post(f"/api/v1/chat?character_id={character_id}", headers=headers)
    assert response.status_code == 200

    after_count = db_session.query(Character).filter(Character.character_id == character_id).first().character_usage_count
    assert after_count == before_count + 1

def test_get_characters_rank(client: TestClient, db_session: Session):
    response = client.get("/api/v1/characters/rank/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 5

def test_update_character_deactivate(client: TestClient, db_session: Session):
    headers = get_token(client)

    response = client.get("/api/v1/characters/me/", headers=headers)
    assert response.status_code == 200
    character_id = response.json()[-1]['characterId']

    response = client.put(
        f"/api/v1/characters/{character_id}/deactivate", 
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Character deactivated successfully"

    response = client.get("/api/v1/characters/me/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    character_list = [character.get("characterId") for character in data]
    assert character_id not in character_list

    updated_character = db_session.query(Character).filter(Character.character_id == character_id).first()
    assert updated_character.character_is_active == False
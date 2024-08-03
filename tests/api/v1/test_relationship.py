from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session
from app.models.characters import Character

from tests.get_token import get_token

@pytest.fixture
def client(client: TestClient) -> TestClient:
    return client

def test_create_relationship(client: TestClient):
    create_relationship = {"relationshipName": "test relation"}
    
    response = client.post(f"/api/v1/relationship", json=create_relationship)
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == "Relationship created successfully"

def test_get_relationships(client: TestClient):
    response = client.get(f"/api/v1/relationship/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_update_relationship(client: TestClient):
    response = client.get(f"/api/v1/relationship/")
    assert response.status_code == 200
    data = response.json()
    relationship_id = data[0]['relationshipId']

    update_relationship = {"relationshipName": "update relation"}

    response = client.put(f"/api/v1/relationship/{relationship_id}", json=update_relationship)
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == "Relationship updated successfully"

    response = client.get(f"/api/v1/relationship/")
    assert response.status_code == 200
    data = response.json()
    assert [relationship['relationshipName'] for relationship in data if relationship['relationshipId'] == relationship_id][0] == "update relation"

def test_delete_relationship(client: TestClient):
    response = client.get(f"/api/v1/relationship/")
    assert response.status_code == 200
    data = response.json()
    relationship_id = data[0]['relationshipId']

    response = client.delete(f"/api/v1/relationship/{relationship_id}")
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == "Relationship deleted successfully"

    response = client.get(f"/api/v1/relationship/")
    assert response.status_code == 200
    data = response.json()
    assert relationship_id not in [relationship['relationshipId'] for relationship in data]

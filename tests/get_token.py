from fastapi.testclient import TestClient


def get_token(client: TestClient):
    response = client.post("/api/v1/auth/token/test")
    assert response.status_code == 200
    test_token = response.json().get("jwtToken")

    return {"Authorization": f"Bearer {test_token}"}
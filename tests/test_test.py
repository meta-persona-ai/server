from fastapi.testclient import TestClient
import pytest
import logging

logger = logging.getLogger('test')

@pytest.fixture
def client(client: TestClient) -> TestClient:
    return client

def test_my_test(client):
    logger.warning("log test")
